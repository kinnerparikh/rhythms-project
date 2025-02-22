import sqlite3
from app.core.config import settings
import typing, time
from datetime import date

# ---- Slack Bolt ----
from slack_bolt import App, Say
from slack_bolt.adapter.fastapi import SlackRequestHandler

from app.services.azure_service import AzureService
from app.services.github_service import GitHubService

app = App(token=settings.SLACK_BOT_TOKEN, signing_secret=settings.SLACK_SIGNING_SECRET)
app_handler = SlackRequestHandler(app)
azure_service = AzureService()
github_service = GitHubService()

stop_completions = False

@app.event("app_mention")
def handle_app_mention(body, say):
    print(body['event']['text'].split('>')[1].strip())
    user = body['event']['user']
    print(user)

@app.event("message")
def handle_message(message: typing.Dict, say: Say):
    print(message)
    if (message['channel_type'] == 'im'):
        if (stop_completions):
            return
        response = azure_service.get_completion(
            prompt=message["text"],
            user_id=message["user"],
            thread_id=message["thread_ts"].split(".")[0]
        )
        say(response)

def new_thread(channel_id: str, user_id: str, context: str = None):
    say = Say(client=app.client, channel=channel_id)
    say.thread_ts = str(int(time.time()))

    current_date = date.today()
    formatted_date = current_date.strftime("%B %d, %Y")

    def convert_date(date_str):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ'))
    commits = []
    for i in github_service.get_commits("rhythms-project"):
        date_local = convert_date(i["commit"]["author"]["date"])
        commits.append(date_local + " " + i["commit"]["message"])
    
    issues = []
    for i in github_service.get_issues("rhythms-project"):
        if i["state"] == "open":
            issues.append(i["title"] + ", issued on " + convert_date(i["created_at"]))
        if i["state"] == "closed":
            issues.append(i["title"] + ", closed on " + convert_date(i["closed_at"]))


    if stop_completions:
        say("new thread")
        return
    response = azure_service.get_completion(
        prompt=f"***INIT*** \nDATE!!!{formatted_date}!!! \nrecent commits: {commits}, open issues: {issues}\n***ENDINIT***",
        user_id=user_id,
        thread_id=say.thread_ts
    )

    say(response)

# ---- FastAPI ----
from fastapi import FastAPI, Request
from app.models.requests import NewChat

api = FastAPI()

#USERID: U08E538DSBB

# @api.get(settings.API_V1_STR + "/getgitissues")
# def get_git_issues():
#     resp = github_service.get_issues("rhythms-project")
#     for issue in resp:
#         if issue["state"] == "open":
#             print(issue["title"] + ", issued on " + issue["created_at"])
#         if issue["state"] == "closed":
#             print(issue["title"] + ", closed on " + issue["closed_at"])
#     return resp

@api.post(settings.API_V1_STR + "/newchat")
def new_chat(request: NewChat):
    resp = app.client.conversations_open(users=request.user_id)
    if resp['ok']:
        channel_id = resp['channel']['id']
    else:
        return {"error": resp['error']}
    new_thread(channel_id, request.user_id, context=request.context)

@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)