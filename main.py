from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from app.core.config import settings
# from app.api.routes import router
from app.core.config import settings
from app.services.azure_service import AzureService
from app.services.slack_service import start
from app.services.github_service import GitHubService
from app.models.requests import CompletionRequest, SlackMessageRequest
import os


app = FastAPI(
    title="Standup Bot",
    description="Intelligent assistant for collecting standup updates",
    version="1.0.0"
)

# Initialize services
try:
    slack_app = start()
    azure_service = AzureService()
    # github_service = GitHubService()
except Exception as e:
    print(f"Error initializing services: {str(e)}")
    
@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/api/v1/azure/completion")
async def get_completion(request: CompletionRequest):
    """
    Get a completion from Azure OpenAI
    """
    try:
        response = azure_service.get_completion(
            prompt=request.prompt,
            system_message=request.system_message
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/slack/message")
async def send_slack_message(request: SlackMessageRequest):
    """
    Send a message to a Slack channel
    """
    try:
        response = slack_app.client.chat_postMessage(
            channel=request.channel,
            text=request.message
        )
        return {"message_ts": response["ts"], "channel": response["channel"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

