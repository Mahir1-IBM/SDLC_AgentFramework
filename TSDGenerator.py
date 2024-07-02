from check_status_and_download_docx import check_status_and_download_docx
from get_section_mapping_and_upload_file import get_section_mapping_and_upload_file
from autogen import ConversableAgent, config_list_from_json
from langchain_community.document_loaders import PyMuPDFLoader
from ibm_docx_parser import extract_text, extract_text_with_image_reference, get_resource, extract_text_with_base64_image


config_list = config_list_from_json(
    env_or_file = "OAI_CONFIG_LIST.json"
)

llm_config = {
    "config_list" : config_list, 
    "timeout" : 120
}
 
def TSDGenerator() -> str:
    TSD_bot = ConversableAgent(
        name="TSD_bot",
        system_message="Download the TSD (Techincal Specification Document) by calling the APIs. Do not return back the code.",
        llm_config=llm_config
    )

    user_proxy = ConversableAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        system_message="Interact with TSD_bot and get the TSD as docx document. Make sure the TSD is downloaded locally and store it in /Users/mahir/Desktop/Agents/Application. Do not ask for the code but the document itself.",
        max_consecutive_auto_reply=2,
    )

    TSD_bot.register_for_llm(name="get_section_mapping_and_upload_file", description="Posting the request for genertaing the TSD by uploading rewuired files.")(get_section_mapping_and_upload_file)
    TSD_bot.register_for_llm(name="check_status_and_download_docx", description="function/Tool to check the status of generated TSD and download it locally.")(check_status_and_download_docx)

    user_proxy.register_for_execution(name="get_section_mapping_and_upload_file")(get_section_mapping_and_upload_file)
    user_proxy.register_for_execution(name="check_status_and_download_docx")(check_status_and_download_docx)

    user_proxy.initiate_chat(TSD_bot, message="Generate the TSD and download it to '/Users/mahir/Desktop/Agents/Application/TSD.docx'.")

    data = extract_text("/Users/mahir/Desktop/Agents/Application/TSD.docx")
    return data

