from typing import Annotated, List, TypedDict
import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph, add_messages
from app.core.config import settings
from mem0 import MemoryClient

class AzureService:
    def __init__(self):
        self._validate_environment()
        model = init_chat_model("gpt-4o", model_provider="openai", api_key=settings.OPENAI_KEY)
        mem0 = MemoryClient(settings.MEM0_API_KEY)

        base_prompt = "You are an intelligent assistant that help collect daily standup updates. You should focus on natural conversations and reducing user workload through automated drafting. In these standups, you should cover: accomplishments since last standup, plans for today, and any blockers or challenges that are currently being faced. \nFollowing is data that you will use to provide these updates. *Github Issues, Github Commits*\nYou should ask questions, if needed, about any blockers, or if there is a task that I taking more than a 3 days to resolve. If the answer to these questions is unclear, ask follow up questions. If the prompt starts with ***INIT***, then start your message with the date provided in the prompt between the !!! symbols followed by a new line."

        # template = ChatPromptTemplate.from_messages(
        #     [
        #         ("system", base_prompt),
        #         MessagesPlaceholder(variable_name="messages")
        #     ]
        # )
        class State(TypedDict):
            messages: Annotated[List[HumanMessage | AIMessage], add_messages]
            mem0_user_id: str

        self.workflow = StateGraph(state_schema=State)

        def call_model(state: State):
            messages = state["messages"]
            user_id = state["mem0_user_id"]

            memories = mem0.search(messages[-1].content, user_id=user_id)
            print(memories)

            context = "Relevant information from previous conversations:\n"
            for memory in memories:
                context += f"- {memory['memory']}\n"

            system_message = SystemMessage(content=base_prompt + context)

            full_message = [system_message] + messages

            response = model.invoke(full_message)

            mem0.add(f"User: {messages[-1].content}\nAssistant: {response.content}", user_id=user_id, output_format="v1.1")
            return {"messages": response}


        self.workflow.add_node("model", call_model)
        self.workflow.add_edge(START, "model")
        # self.workflow.add_edge("model", "model")

        memory = MemorySaver()
        self.app = self.workflow.compile(checkpointer=memory)

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
    

    def get_completion(self, prompt: str, user_id: str, thread_id: str = None, system_message: str = None) -> str:
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
        state = {"messages": input_messages, "mem0_user_id": user_id}
        config = {'configurable': {"thread_id": user_id + "_" + thread_id}}

        response = "No response"
        for event in self.app.stream(state, config):
            for value in event.values():
                if value.get("messages"):
                    # print(value["messages"])
                    response = value["messages"].content

        return response