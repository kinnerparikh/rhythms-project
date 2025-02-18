from app.core.config import settings
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=settings.SLACK_BOT_TOKEN)

@app.message("hello")
def message_hello(message, say):
    say(f"Hey there <@{message['user']}>!")

def start():
    SocketModeHandler(app, settings.SLACK_APP_TOKEN).start()

if __name__ == "__main__":
    start()