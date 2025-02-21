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

stop_completions = True

@app.event("message")
def handle_message(message: typing.Dict, say: Say):
    print(message)
    if (message['channel_type'] == 'im'):
        if (stop_completions):
            return
        response = azure_service.get_completion(
            prompt=message["text"],
            thread_id=message["thread_ts"].split(".")[0]
        )
        say(response)
    else:
        print("Not a DM, ignoring")

def new_thread(channel_id: str, context: str = None):
    say = Say(client=app.client, channel=channel_id)
    say.thread_ts = int(time.time())

    current_date = date.today()
    formatted_date = current_date.strftime("%B %d, %Y")

    commits = []

    for i in github_service.get_commits("rhythms-project"):
        date_zulu = i["commit"]["author"]["date"]
        date_local = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(date_zulu, '%Y-%m-%dT%H:%M:%SZ'))
        commits.append(date_local + " " + i["commit"]["message"])
    
    issues = []
    for i in github_service.get_issues("rhythms-project"):
        issues.append(i["title"])


    if stop_completions:
        say("new thread")
        return
    response = azure_service.get_completion(
        prompt=f"***INIT*** \nDATE!!!{formatted_date}!!! \nrecent commits: {commits}, open issues: {issues}\n***ENDINIT***",
        thread_id=say.thread_ts
    )

    say(response)

# ---- FastAPI ----
from fastapi import FastAPI, Request
from app.models.requests import NewChat

api = FastAPI()

#USERID: U08E538DSBB

@api.post("/api/v1/newchat")
def new_chat(request: NewChat):
    resp = app.client.conversations_open(users=request.user_id)
    if resp['ok']:
        channel_id = resp['channel']['id']
    else:
        return {"error": resp['error']}
    new_thread(channel_id, context=request.context)

@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)