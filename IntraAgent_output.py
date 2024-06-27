import warnings

from TSDGenerator import TSDGenerator
from testingTSD import testing
from autogen import ConversableAgent, config_list_from_json

warnings.filterwarnings("ignore")

config_list = config_list_from_json(
    env_or_file = "OAI_CONFIG_LIST.json"
)

llm_config = {
    "config_list" : config_list, 
    "timeout" : 120
}


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

user_proxy.initiate_chat(
    IntraAgent, message= f"Generate the TSD and verify it.")

