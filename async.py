import time
import asyncio
import warnings
from ibm_docx_parser import extract_text
from typing_extensions import Annotated
from autogen import UserProxyAgent, config_list_from_json, AssistantAgent, GroupChat, GroupChatManager
from autogen.cache import Cache
import agentops
import os
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# Initialize AgentOps
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
if not AGENTOPS_API_KEY:
    raise ValueError("AGENTOPS_API_KEY not found in environment variables")

agentops.init(AGENTOPS_API_KEY)

@agentops.record_function('main')
def main():
    start_time = time.time()

    config_list = config_list_from_json(
        env_or_file = "OAI_CONFIG_LIST.json"
    )

    llm_config = {
        "config_list" : config_list, 
        "timeout" : 120
    }

    data = extract_text("/Users/mahir/Desktop/Agents/Application/TSD.docx")

    assistant1 = AssistantAgent(
        name="Summarizer_1",
        system_message="Summarize the given document, read it completely and return back a concise and relevant summary of the document. Use summary function; Add TERMINATE to the end of the summary report;",
        llm_config=llm_config
    )

    assistant2 = AssistantAgent(
        name="Summarizer_2",
        system_message="Summarize the given document, read it completely and return back a concise and relevant summary of the document. Use summary function; Add TERMINATE to the end of the summary report;",
        llm_config=llm_config
    )

    assistant3 = AssistantAgent(
        name="Summarizer_3",
        system_message="Summarize the given document, read it completely and return back a concise and relevant summary of the document. Use summary function; Add TERMINATE to the end of the summary report;",
        llm_config=llm_config
    )

    user_proxy = UserProxyAgent(
        name="user_proxy",
        system_message="Make sure to divide the input document into three equal parts and give each part text to one of the assistants. Collect output from each and concatenate them to obtain full summary.",
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
        code_execution_config=False,
    )

    @agentops.record_function('summary')
    @user_proxy.register_for_execution()
    @assistant1.register_for_llm(description="Summarize the given text in a concise manner")
    @assistant2.register_for_llm(description="Summarize the given text in a concise manner")
    @assistant3.register_for_llm(description="Summarize the given text in a concise manner")
    def summary(
            data : Annotated[str, "data that needs to be summarized."]
        ) -> str:

        assistant = AssistantAgent(
            name="Summarizer",
            system_message="Summarize the given text, read it completely and return back a concise and relevant summary of the particular text; Add TERMINATE at the end of task.",
            llm_config=llm_config
        )

        user_proxy = UserProxyAgent(
            name="user",
            is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
            human_input_mode="NEVER",
            system_message="Interact with assistant and make sure it completes the task.",
            code_execution_config=False,
            max_consecutive_auto_reply = 1,
        )

        user_proxy.initiate_chat(assistant, message = f"Give me a summary of {data}")

        return user_proxy.last_message()["content"]

    @agentops.record_function('terminate_group_chat')
    @user_proxy.register_for_execution()
    @assistant1.register_for_llm(description="terminate the group chat")
    @assistant2.register_for_llm(description="terminate the group chat")
    @assistant3.register_for_llm(description="terminate the group chat")
    def terminate_group_chat(message: Annotated[str, "Message to be sent to the group chat."]) -> str:
        return f"[GROUPCHAT_TERMINATE] {message}"

    groupchat = GroupChat(agents=[user_proxy, assistant1, assistant2, assistant3], messages=[], max_round=12)

    llm_config_manager = llm_config.copy()
    llm_config_manager.pop("functions", None)
    llm_config_manager.pop("tools", None)

    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config_manager,
        is_termination_msg=lambda x: "GROUPCHAT_TERMINATE" in x.get("content", ""),
    )

    @agentops.record_function('initiate_chat')
    async def initiate_chat():
        with Cache.disk() as cache:
            await user_proxy.a_initiate_chat(  
                manager,
                message = f"Divide {data} in three equal parts and give each to each agent. Get summary from all the agents and concatenate them. Give final summary.",
                cache=cache,
            )

    asyncio.run(initiate_chat())

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        agentops.log_error(str(e))
    finally:
        agentops.end_session('Success')