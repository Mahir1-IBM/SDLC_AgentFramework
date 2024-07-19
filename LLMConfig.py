from autogen import config_list_from_json

config_list = config_list_from_json(
    env_or_file = "OAI_CONFIG_LIST.json"
)


llm_config_fsd = {
    "functions": [
        {
            "name": "testingFSD",
            "description": "For verification of the Functional Specification Document (FSD). It returns a list of parmeters/filters which input FSD fails to staisfy",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "string",
                            "description": "FSD data that needs to be verified. FSD will be input by user",
                        },
                    },
                "required": ["data"],
            },
        },
    ],
    "config_list": config_list

}

llm_config_coder = {
    "functions": [
        {
            "name": "codeOutputCheck",
            "description": "Generates the SAP ABAP Code using the TSD and also validates the code produced.",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "WRICEF_type": {
                            "type": "string",
                            "description": "The type of WRICEF of TSD : Reports or Enhancements or Interfaces.",
                        },
                    },
                "required": ["WRICEF_type"],
            },
        },
    ],
    "config_list": config_list
}

