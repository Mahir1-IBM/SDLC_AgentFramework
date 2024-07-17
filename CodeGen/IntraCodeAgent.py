import warnings

from CodeGen import CodeGenAPI
from CodeValidation import testingCode
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
                        "WRICEFtype": {
                            "type": "string",
                            "description": "The wricef type of the TSD.",
                        },
                        "input_file_path": {
                            "type": "string",
                            "description": "The path where the TSD is stored.",
                        }
                    },
                "required": ["WRICEFtype", "input_file_path"],
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


IntraAgent = ConversableAgent(
    name="IntraAgent",
    system_message="Generate the SAP ABAP code from the given Techincal Specification Document by using the CodeGenAPI function. Use the parameters given in the message. Then return the list of parameters that the generated code is failing at, by using the testingCode function. Reply TERMINATE when your task is done",
    llm_config=llm_config_intra_agent
)


user_proxy = ConversableAgent(
    name="user_proxy",
    system_message="Use the parameters/arguments given and send them to the IntraAgent to be used for generation and validation of the ABAP code. Get the list of parameters which are not satisfied by code.",
    max_consecutive_auto_reply= 2,
    human_input_mode="TERMINATE",
    function_map={
        "CodeGenAPI": CodeGenAPI,
        "testingCode": testingCode,
    }
)


user_proxy.initiate_chat(
    IntraAgent, message= f"Generate the ABAP code by the given TSD using the arguments, that are WRICEFtype = 'Enhancement', input_file_path of TSD = 'O2C_E_826_827_Product Allocation UK_TDS.docx'. Verify the code too")


print(user_proxy.last_message()["content"])