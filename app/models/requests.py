from pydantic import BaseModel

class CompletionRequest(BaseModel):
    prompt: str
    system_message: str | None = None

class SlackMessageRequest(BaseModel):
    channel: str
    message: str 