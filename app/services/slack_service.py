from app.core.config import settings
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from app.services.azure_service import AzureService

app = App(token=settings.SLACK_BOT_TOKEN)
azure_service = AzureService()

@app.message("")
def respond_to_any_message(message, say):
    print(str(message["text"]))

    response = azure_service.get_completion(
        prompt=message["text"],
        thread_id=message["thread_ts"].split(".")[0]
    )

    say(response)

    

def start():
    SocketModeHandler(app, settings.SLACK_APP_TOKEN).start()

if __name__ == "__main__":
    start()