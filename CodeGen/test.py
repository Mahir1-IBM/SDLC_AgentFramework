import os
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

config_list = config_list_from_json(
    env_or_file = "../OAI_CONFIG_LIST.json"
)

llm_config = {
    "config_list" : config_list, 
    "timeout" : 120
}


assistant = AssistantAgent("assistant", llm_config=llm_config)
user_proxy = UserProxyAgent("user_proxy", code_execution_config=False)

# Start the chat
user_proxy.initiate_chat(
    assistant,
    message="Make some puns on the word 'devina' in hinglish.",
)