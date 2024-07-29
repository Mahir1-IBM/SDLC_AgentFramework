from autogen import config_list_from_json

config_list = config_list_from_json(
    env_or_file = "OAI_CONFIG_LIST.json"
)

llm_config = {
    "config_list" : config_list, 
    "timeout" : 120
}

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


# //////////////////////////// Config for verification of FSD //////////////////////////// 

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

# ///////////////// Config for Generation and verifiction of ABAP code from TSD //////////////////////

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

llm_config_test = {
    "functions": [
        {
            "name": "ReadingDocx",
            "description": "For reading the Technical Specification Document (TSD) given in docx format",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Name and path of TSD file.",
                        },
                    },
                "required": ["path"],
            },
        },
        {
            "name": "create_file",
            "description": "For reading the Technical Specification Document (TSD) given in docx format",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Name and path of file to create.",
                        },
                        "text": {
                            "type": "string",
                            "description": "Text to write in the file",
                        },
                    },
                "required": ["filename", "text"],
            },
        },
    ],
    "config_list": config_list
}

llm_config_test_2 = {
    "functions": [
        {
            "name": "testing",
            "description": "For verification of the Techincal Specification Document (TSD). It returns a list of parmeters/filters which generated TSD lacked",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "number": {
                            "type": "integer",
                            "description": "Index of parameter list",
                        },
                        "data": {
                            "type": "string",
                            "description": "TSD in text form when available",
                        },
                    },
                "required": ["number", "data"],
            },
        },
        {
            "name": "create_file",
            "description": "For reading the Technical Specification Document (TSD) given in docx format",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "Path": {
                            "type": "string",
                            "description": "Path of file to create.",
                        },
                        "number": {
                            "type": "integer",
                            "description": "Name of file to create.",
                        },
                        "text": {
                            "type": "string",
                            "description": "Revised TSD text to be written in the file.",
                        },
                    },
                "required": ["Path", "number", "text"],
            },
        }
    ],
    "config_list": config_list
}

llm_config_generator = {
    "functions": [
        {
            "name": "generating",
            "description": "For generating of the Techincal Specification Document (TSD). It returns a new TSD in text form.",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "Data": {
                            "type": "string",
                            "description": "TSD in text form when available for reference",
                        },
                        "params": {
                            "type": "string",
                            "description": "Parameters that TSD need to satisfy",
                        },
                    },
                "required": ["Data", "params"],
            },
        }
    ],
    "config_list": config_list
}

llm_config_split = {
    "functions": [
        {
            "name": "split_document",
            "description": "For splitting a document into 3 equal parts. It returns three text files",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "path of the document",
                        }
                    },
                "required": ["path"],
            },
        }
    ],
    "config_list": config_list
}

llm_config_saver = {
    "functions": [
        {
            "name": "create_file",
            "description": "For reading the Technical Specification Document (TSD) given in docx format",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "Path": {
                            "type": "string",
                            "description": "Path of file to create.",
                        },
                        "number": {
                            "type": "integer",
                            "description": "Name of file to create.",
                        },
                        "text": {
                            "type": "string",
                            "description": "Revised TSD text to be written in the file.",
                        },
                    },
                "required": ["Path", "number", "text"],
            },
        }
    ],
    "config_list": config_list
}

# llm_config_scraping_agent = {
#     "functions": [
#         {
#             "name": "verification_Scraping",
#             "description": "For verification of the Techincal Specification Document (TSD). It returns a list of parmeters/filters which generated TSD lacked",
#             "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "data": {
#                             "type": "string",
#                             "description": "TSD data that needs to be verified.",
#                         },
#                         "params": {
#                             "type": "string",
#                             "description": "List of parameters that TSD does not verify",
#                         },
#                     },
#                 "required": ["data", "params"],
#             },
#         },
#     ],
#     "config_list": config_list
# }