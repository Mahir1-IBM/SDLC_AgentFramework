import warnings
import streamlit as st

import Application/TSDGenerator.py as TSDGenerator
from TSDGenerator import TSDGenerator
from testingTSD import testing
from autogen import ConversableAgent, config_list_from_json

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

IntraAgent = ConversableAgent(
    name="IntraAgent",
    system_message="Download the TSD (Techincal Specification Document) by using the TSDGenerator function. Then return the list of parameters that the generated TSD is failing at, by using the testing function.Reply TERMINATE when your task is done",
    llm_config=llm_config_intra_agent
)

user_proxy = ConversableAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    function_map={
        "TSDGenerator": TSDGenerator,
        "testing": testing,
    }
)

st.title("TSD Generation and Verification")

if st.button("Generate and Verify TSD"):
    user_proxy.initiate_chat(IntraAgent, message="Generate the TSD and verify it.")

    with st.spinner('Generating and verifying TSD...'):
        while True:
            response = user_proxy.auto_reply(IntraAgent)
            if response == "TERMINATE":
                break

    st.success('TSD Generation and Verification Completed')
    
    # Display results from the TSD generation and verification
    result = IntraAgent.history[-1]  # Assuming the last message contains the verification result
    st.write("Verification Result:", result)

    # Save the verification result to a log file
    with open('verification_result.log', 'w') as f:
        f.write(result)

