import warnings

from CodeGen.Codegen import CodeGenAPI
from CodeGen.CodeValidation import testingCode
from typing import Annotated
from autogen import ConversableAgent, config_list_from_json


warnings.filterwarnings("ignore")

config_list = config_list_from_json(
    env_or_file = "/Users/mahir/Desktop/Agents/Application/OAI_CONFIG_LIST.json"
)

llm_config = {
    "config_list" : config_list, 
    "timeout" : 120
}


llm_config_intra_agent = {
    "functions": [
        {
            "name": "CodeGenAPI",
            "description": "Function for generating the SAP ABAP code using Techincal Specification document(TSD). It returns the generated code as json",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "WRICEF_type": {
                            "type": "string",
                            "description": "The wricef type of the TSD.",
                        },
                        "input_file_path": {
                            "type": "string",
                            "description": "The path where the TSD is stored.",
                        }
                    },
                "required": ["WRICEF_type", "input_file_path"],
            },
        },
        {
            "name": "testingCode",
            "description": "For verification of the generate SAP ABAP code. It returns a list of parmeters/filters which were not staisfied by the generated ABAP code",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "ABAP code in json format",
                        },
                    },
                "required": ["code"],
            },
        },
    ],
    "config_list": config_list
}


def codeOutputCheck(
        WRICEF_type: Annotated[str, "The wricef type of the TSD."],
    ) -> str:
    
    IntraAgent = ConversableAgent(
        name="IntraCodeAgent",
        system_message="Generate the SAP ABAP code from the given Techincal Specification Document by using the CodeGenAPI function. Then return the list of parameters that the generated code is failing at, by using the testingCode function. Reply TERMINATE when your task is done",
        llm_config=llm_config_intra_agent
    )

    user_proxy = ConversableAgent(
        name="user_proxy",
        max_consecutive_auto_reply= 2,
        human_input_mode="TERMINATE",
        function_map={
            "CodeGenAPI": CodeGenAPI,
            "testingCode": testingCode,
        }
    )

    user_proxy.initiate_chat(
        IntraAgent, message= f"Generate and verify the ABAP code by the given TSD using the arguments : WRICEF_type = {WRICEF_type}; input_file_path = '/Users/mahir/Desktop/Agents/Application/TSD.docx'.")


    return (user_proxy.last_message()["content"])


# print(codeOutputCheck("Report"))