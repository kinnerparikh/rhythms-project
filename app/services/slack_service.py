from app.core.config import settings
from slack_bolt import App
from slack_bolt.context.say import Say
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import date
import time

from app.services.azure_service import AzureService
from app.services.github_service import GitHubService

app = App(token=settings.SLACK_BOT_TOKEN)
azure_service = AzureService()
github_service = GitHubService()


@app.message("newchat")
def new_chat(message, say):

    # this is kinda hacky but it works
    # creates a new thread by setting the thread_ts to the current timestamp
    # this is because the thread_ts is required to be unique
    curr_ts = int(time.time())
    say.thread_ts = curr_ts

    
    current_date = date.today()
    formatted_date = current_date.strftime("%B %d, %Y")

    response = azure_service.get_completion(
        prompt=f"***INIT*** DATE!!!{formatted_date}!!! ***ENDINIT***",
        thread_id=curr_ts
    )

    say(response)

    

@app.message("")
def respond_to_any_message(message, say: Say):
    print(str(message["text"]))

    response = azure_service.get_completion(
        prompt=message["text"],
        thread_id=message["thread_ts"].split(".")[0]
    )

    say(response)


    


def start():
    # print(github_service.get_issues("kinnerparikh/standup-bot"))
    SocketModeHandler(app, settings.SLACK_APP_TOKEN).start()


if __name__ == "__main__":
    start()