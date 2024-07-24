from autogen import config_list_from_json

config_list = config_list_from_json(
    env_or_file = "OAI_CONFIG_LIST.json"
)

llm_config = {
    "config_list" : config_list, 
    "timeout" : 120
}


# ///////////////// Config for Generation and verifiction of ABAP code from TSD //////////////////////

llm_config_code_agent = {
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

