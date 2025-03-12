from pydantic_settings import BaseSettings
from typing import Optional

class Config(BaseSettings):
    # API Configs
    API_V1_STR: str = "/api/v1"

    # Slack
    SLACK_BOT_TOKEN: str
    # SLACK_APP_TOKEN: str
    SLACK_SIGNING_SECRET: str
    # GitHub
    GITHUB_TOKEN: Optional[str] = None
    GITHUB_APP_ID: str
    GITHUB_REPO: str
    GITHUB_APP_PRIVATE_KEY_LOC: str

    # Linear
    LINEAR_API_KEY: Optional[str] = None
    # Azure OpenAI
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str
    AZURE_OPENAI_API_VERSION: str
    OPENAI_KEY: str

    LANGSMITH_TRACING: str
    LANGSMITH_API_KEY: str

    MEM0_API_KEY: str
    
    class Config:
        env_file = ".env"

settings = Config()