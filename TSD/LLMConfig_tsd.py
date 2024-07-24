from autogen import config_list_from_json

config_list = config_list_from_json(
    env_or_file = "OAI_CONFIG_LIST.json"
)

llm_config = {
    "config_list" : config_list, 
    "timeout" : 120
}

# ////////////////////////////////// Config for Generation of TSD /////////////////////////////////

llm_config_tsd = {
        "functions": [
            {
                "name": "get_section_mapping_and_upload_file",
                "description": "Posting the request for genertaing the TSD by uploading rewuired files.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user id of the user.",
                        },
                        "tsd_type": {
                            "type": "string",
                            "description": "The type of TSD to be generated : initial or final.",
                        },
                        "WRICEF_type": {
                            "type": "string",
                            "description": "The type of WRICEF to be used : Reports or Enhancements or Interfaces.",
                        },
                        "input_file_path": {
                            "type": "string",
                            "description": "The path where FSD is stored.",
                        },
                    },
                    "required": ["user_id", "tsd_type", "WRICEF_type", "input_file_path"],
                },
            },
            {
                "name": "check_status_and_download_docx",
                "description": "function/Tool to check the status of generated TSD and download it locally.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user id of the user.",
                        },
                        "output_path": {
                            "type": "string",
                            "description": "The path where the generated TSD is saved locally.",
                        },
                    },
                    "required": ["output_path, user_id"],
                },
            },
        ],
        "config_list": config_list
    }


# ///////////////// Config for Generation and verifiction of TSD from FSD //////////////////////

llm_config_intra_agent = {
    "functions": [
        {
            "name": "TSDGenerator",
            "description": "Function for generating the Techincal Specification Document (TSD). It returns the generated TSD as text",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user id of the user.",
                        },
                        "tsd_type": {
                            "type": "string",
                            "description": "The type of TSD to be generated : initial or final.",
                        },
                        "WRICEF_type": {
                            "type": "string",
                            "description": "The type of WRICEF to be used : Reports or Enhancements or Interfaces.",
                        },
                        "input_file_path": {
                            "type": "string",
                            "description": "The path where FSD is stored.",
                        },
                    },
                "required": ["user_id", "tsd_type", "WRICEF_type", "input_file_path"],
            },
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
        }
    ],
    "config_list": config_list
}