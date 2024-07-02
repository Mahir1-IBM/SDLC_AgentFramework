
import streamlit as st
import asyncio
import warnings

from TSDGenerator import TSDGenerator
from testingTSD import testing

from autogen import config_list_from_json, ConversableAgent

warnings.filterwarnings("ignore")

config_list = config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json"
)

llm_config_intra_agent = {
    "functions": [
        {
            "name": "TSDGenerator",
            "description": "Function for generating the Techincal Specification Document (TSD). It returns the generated TSD as text"
        },
        {
            "name": "testing",
            "description": "For verification of the Techincal Specification Document (TSD). It returns a list of parmeters/filters which generated TSD lacked",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "TSD in text form when available",
                    },
                },
                "required": ["data"],
            },
        },
    ],
    "config_list": config_list
}

st.set_page_config(page_title="Intra Output Chat app", page_icon="🤖", layout="wide")

st.title("Intra Output Agent")

class TrackableAssistantAgent(ConversableAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            if isinstance(message, dict):
                st.json(message)
            else:
                st.markdown(message)
        return super()._process_received_message(message, sender, silent)


class TrackableUserProxyAgent(ConversableAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            if isinstance(message, dict):
                st.json(message)
            else:
                st.markdown(message)
        return super()._process_received_message(message, sender, silent)


config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

llm_config = {
    "config_list": config_list,
    "timeout": 120,
    "seed": 42, 
    "temperature": 0, 
}

with st.container():
    user_input = st.text_input("User Input")
    if user_input:

        assistant = TrackableAssistantAgent(
            name="IntraAgent",
            system_message="Download the TSD (Techincal Specification Document) by using the TSDGenerator function. Then return the list of parameters that the generated TSD is failing at, by using the testing function.Reply TERMINATE when your task is done",
            llm_config=llm_config_intra_agent
        )

        user_proxy = TrackableUserProxyAgent(
            name="user",
            human_input_mode="NEVER",
            is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
            function_map={
                "TSDGenerator": TSDGenerator,
                "testing": testing,
            }
        )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def initiate_chat():
            await user_proxy.a_initiate_chat(assistant, message=user_input)

        loop.run_until_complete(initiate_chat())



st.stop()