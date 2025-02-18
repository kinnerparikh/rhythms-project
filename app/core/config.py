from pydantic_settings import BaseSettings
from typing import Optional

class Config(BaseSettings):
    # API Configs
    API_V1_STR: str = "/api/v1"

    # Slack
    SLACK_BOT_TOKEN: str
    SLACK_APP_TOKEN: str
    # GitHub
    GITHUB_TOKEN: Optional[str] = None
    # Linear
    LINEAR_API_KEY: Optional[str] = None
    # Azure OpenAI
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str
    AZURE_OPENAI_API_VERSION: str

    LANGSMITH_TRACING: str
    LANGSMITH_API_KEY: str
    
    class Config:
        env_file = ".env"

settings = Config()