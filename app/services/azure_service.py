import getpass
import os
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

class AzureService:
    def __init__(self):
        self._validate_environment()
        model = AzureChatOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
            openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        )

        template = ChatPromptTemplate.from_messages(
            [
                ("system", "you talk like a valley girl"),
                MessagesPlaceholder(variable_name="messages")
            ]
        )
        workflow = StateGraph(state_schema=MessagesState)

        def call_model(state: MessagesState):
            prompt = template.invoke(state)
            response = model.invoke(prompt)
            return {"messages": response}

        workflow.add_edge(START, "model")
        workflow.add_node("model", call_model)

        memory = MemorySaver()
        self.app = workflow.compile(checkpointer=memory)

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
    

    def get_completion(self, prompt: str, thread_id: str = None, system_message: str = None) -> str:
        """
        Get a completion from Azure OpenAI
        
        Args:
            prompt (str): The user's prompt
            thread_id (str, optional): The thread ID to set context
            system_message (str, optional): System message to set context
            
        Returns:
            str: The model's response
        """

        input_messages = [
            HumanMessage(content=prompt)
        ]

        out = self.app.invoke( {"messages": input_messages}, config={'configurable': {"thread_id": thread_id}} )
        return out['messages'][-1].content