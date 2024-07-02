import time
import warnings
from ibm_docx_parser import extract_text
from typing_extensions import Annotated
from autogen import UserProxyAgent, config_list_from_json, AssistantAgent, ConversableAgent

warnings.filterwarnings("ignore")

start_time = time.time()


config_list = config_list_from_json(
    env_or_file = "OAI_CONFIG_LIST.json"
)

llm_config = {
    "config_list" : config_list, 
    "timeout" : 120
}

data = extract_text("/Users/mahir/Desktop/Agents/Application/TSD.docx")


def summary(
        data : Annotated[str, "data that needs to be summarized."]
    ) -> str:
    assistant = AssistantAgent(
        name="Summarizer",
        system_message="Summarize the given document, read it completely and return back a concise and relevant summary of the document.; Add TERMINATE to the end of the summary report;",
        llm_config=llm_config
    )

    user_proxy = UserProxyAgent(
        name="user",
        human_input_mode="NEVER",
        system_message="Interact with assistant and make sure it completes the task.",
        is_termination_msg=lambda x: x.get("content", "") and x.get(
                "content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False,
        max_consecutive_auto_reply = 2,
    )

    user_proxy.initiate_chat(assistant, message = f"Give me a summary of {data}")
    return user_proxy.last_message()["content"]


llm_config_summary = {
    "functions": [
        {
            "name": "summary",
            "description": "Function for generating the summary of given document as text.",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "string",
                            "description": "document in text form when available",
                        },
                    },
                "required": ["data"],
            },
        },
    ],
    "config_list": config_list
}

Agent = ConversableAgent(
    name="Agent",
    system_message="Summarize the document by using the summary function. Reply TERMINATE when your task is done",
    llm_config=llm_config_summary
)

user_proxy = ConversableAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    function_map={
        "summary": summary,
    }
)

user_proxy.initiate_chat(
    Agent, message= f"Summarize the document: {data}")

end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")