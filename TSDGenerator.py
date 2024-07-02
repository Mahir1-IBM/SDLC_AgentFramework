from typing import Annotated
from check_status_and_download_docx import check_status_and_download_docx
from get_section_mapping_and_upload_file import get_section_mapping_and_upload_file
from autogen import ConversableAgent, config_list_from_json
from langchain_community.document_loaders import PyMuPDFLoader
from ibm_docx_parser import extract_text, extract_text_with_image_reference, get_resource, extract_text_with_base64_image


config_list = config_list_from_json(
    env_or_file = "OAI_CONFIG_LIST.json"
)


 
def TSDGenerator(
        user_id: Annotated[str, "The user id of the user."],
        tsd_type: Annotated[str, "The type of TSD to be generated : initial or final."], 
        WRICEF_type: Annotated[str, "The type of WRICEF to be used : Reports or Enhancements or Interfaces."], 
        input_file_path:  Annotated[str, "The path where FSD is stored."]
    ) -> str:

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
        

    TSD_bot = ConversableAgent(
        name="TSD_bot",
        system_message="Download the TSD (Techincal Specification Document) by calling the APIs, Use the parameters given for arguments to APIs. Return back the document",
        llm_config=llm_config_tsd
    )

    user_proxy = ConversableAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        system_message="Interact with TSD_bot and get the TSD as docx document. Make sure the TSD is downloaded locally and store it in /Users/mahir/Desktop/Agents/Application/TSD.docx. Do not ask for the code but the document itself.",
        max_consecutive_auto_reply=2,
        function_map={
            "get_section_mapping_and_upload_file": get_section_mapping_and_upload_file,
            "check_status_and_download_docx": check_status_and_download_docx,
        }
    )

    # TSD_bot.register_for_llm(name="get_section_mapping_and_upload_file", description="Posting the request for genertaing the TSD by uploading rewuired files.")(get_section_mapping_and_upload_file)
    # TSD_bot.register_for_llm(name="check_status_and_download_docx", description="function/Tool to check the status of generated TSD and download it locally.")(check_status_and_download_docx)

    # user_proxy.register_for_execution(name="get_section_mapping_and_upload_file")(get_section_mapping_and_upload_file)
    # user_proxy.register_for_execution(name="check_status_and_download_docx")(check_status_and_download_docx)

    user_proxy.initiate_chat(TSD_bot, message = f"Generate the TSD and download it. Use the parameters given user_id : {user_id}, tsd_type : {tsd_type}, WRICEF_type: {WRICEF_type}, input_file_path: {input_file_path}. Store the path locally in /Users/mahir/Desktop/Agents/Application/TSD.docx.")

    data = extract_text("/Users/mahir/Desktop/Agents/Application/TSD.docx")
    return data

# result = TSDGenerator('Mahir.Jain1@ibm.com', 'Initial', 'report', 'FS RDD0304 - QM _Batch Genealogy Report V1.0 report.docx')
# print("Here the result: ", result)