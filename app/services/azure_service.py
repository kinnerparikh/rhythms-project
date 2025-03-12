from typing import Annotated, List, TypedDict
import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph, add_messages, END
from langgraph.prebuilt import ToolNode, tools_condition, create_react_agent
from app.core.config import settings
from mem0 import MemoryClient
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper

class AzureService:
    def __init__(self):
        self._validate_environment()
        model = init_chat_model("gpt-4o-mini", model_provider="openai", api_key=settings.OPENAI_KEY)
        self.mem0 = MemoryClient(settings.MEM0_API_KEY)


        self.base_prompt = """
            You are an intelligent assistant that help collect daily standup updates. 
            You should focus on natural conversations and reducing user workload through automated drafting. 
            In these standups, you should cover: accomplishments since last standup, plans for today, and any blockers or challenges that are currently being faced.
            Following is data that you will use to provide these updates. 
            *Github Issues, Github Commits*
            You should ask questions, if needed, about any blockers, or if there is a task that I taking more than a 3 days to resolve. 
            If the answer to these questions is unclear, ask follow up questions.
            If the user asks you to perform any actions, complete the action without claficiation or permission if able.
            If the prompt starts with ***INIT***, then start your message with the date provided in the prompt between the !!! symbols followed by a new line.
            Format your responses using slack's markdown syntax.
        """
        # base_prompt = ""

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

        # def call_model(state: State):
        #     messages = state["messages"]
        #     user_id = state["mem0_user_id"]

        #     memories = mem0.search(messages[-1].content, user_id=user_id)

        #     context = "Relevant information from previous conversations:\n"
        #     for memory in memories:
        #         context += f"- {memory['memory']}\n"

        #     system_message = SystemMessage(content=base_prompt + context)

        #     full_message = [system_message] + messages

        #     response = model.invoke(full_message)

        #     mem0.add(f"User: {messages[-1].content}\nAssistant: {response.content}", user_id=user_id, output_format="v1.1")
        #     return {"messages": response}




        private_key = os.open(settings.GITHUB_APP_PRIVATE_KEY_LOC, os.O_RDONLY)
        # make private key a string
        private_key_str = os.read(private_key, 1000000)
        private_key_str = private_key_str.decode("utf-8")
        os.close(private_key)
        github = GitHubAPIWrapper(github_app_id=settings.GITHUB_APP_ID, github_app_private_key=private_key_str, github_repository=settings.GITHUB_REPO)
        toolkit = GitHubToolkit.from_github_api_wrapper(github)
        
        tools = toolkit.get_tools()
        for i in range(len(tools)):
            tools[i].name = tools[i].mode
        
        tool_node = ToolNode(tools)

        # self.workflow.add_node("model", call_model)
        self.workflow.add_node("tools", tool_node)
        self.workflow.add_edge(START, "model")
        self.workflow.add_conditional_edges("model", tools_condition)
        self.workflow.add_edge("tools", "model")
        self.workflow.add_edge("model", END)


        memory = MemorySaver()
        # self.app = self.workflow.compile(checkpointer=memory)

        self.app = create_react_agent(model=model, tools=tools, checkpointer=memory, prompt=SystemMessage(self.base_prompt))

    def _validate_environment(self):
        required_vars = [
            "OPENAI_KEY",
            "MEM0_API_KEY"
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
        memories = self.mem0.search(prompt, user_id=user_id)
        context = "Relevant information from previous conversations:\n"
        for memory in memories:
            context += f"- {memory['memory']}\n"
        input_messages = [
            SystemMessage(content=context),
            HumanMessage(content=prompt)
        ]
        state = {"messages": input_messages}
        config = {'configurable': {"thread_id": user_id + "_" + thread_id}}

        response = "No response"
        events = self.app.stream(state, config, stream_mode="values")
        for event in events:
            response = event["messages"][-1].content
                # if value.get("messages"):
                    # print(value["messages"])
                    # response = value["messages"].content
        
        self.mem0.add(f"User: {prompt}\nAssistant: {response}", user_id=user_id, output_format="v1.1")

        return response