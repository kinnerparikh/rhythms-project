import getpass
import os
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

class AzureService:
    def __init__(self):
        self._validate_environment()
        self.model = AzureChatOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
            openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        )

    def _validate_environment(self):
        required_vars = [
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_DEPLOYMENT_NAME",
            "AZURE_OPENAI_API_VERSION"
        ]
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

    def get_completion(self, prompt: str, system_message: str = None) -> str:
        """
        Get a completion from Azure OpenAI
        
        Args:
            prompt (str): The user's prompt
            system_message (str, optional): System message to set context
            
        Returns:
            str: The model's response
        """
        messages = []
        if system_message:
            messages.append(SystemMessage(system_message))
        messages.append(HumanMessage(prompt))
        
        response = self.model.invoke(messages)
        return response.content