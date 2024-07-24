import streamlit as st
import time
import pyautogui
from typing import Annotated
from autogen import ConversableAgent
from TSD.LLMConfig_tsd import llm_config_tsd
from TSD.check_status_and_download_docx import check_status_and_download_docx
from TSD.get_section_mapping_and_upload_file import get_section_mapping_and_upload_file
from ibm_docx_parser import extract_text, extract_text_with_image_reference, get_resource, extract_text_with_base64_image


def TSDGenerator(
        user_id: Annotated[str, "The user id of the user."],
        tsd_type: Annotated[str, "The type of TSD to be generated : Initial or Final."], 
        WRICEF_type: Annotated[str, "The type of WRICEF to be used : Report or Enhancement or Interface."], 
        input_file_path:  Annotated[str, "The path where FSD is stored."]
    ) -> str:

    TSD_bot = ConversableAgent(
        name="TSD_generating_bot",
        system_message="Download the TSD (Technical Specification Document) by calling the APIs. Use the parameters given for arguments to APIs. Return back the document",
        llm_config=llm_config_tsd
    )

    user_proxy = ConversableAgent(
        name="user_proxy_generationTSD",
        # is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        # human_input_mode="TERMINATE",
        human_input_mode="NEVER",
        # system_message="Interact with TSD_bot and get the TSD as docx document.Do not ask for the code but the document itself.",
        system_message="Interact with TSD_bot and get the TSD as docx document. Make sure the TSD is downloaded locally and store it in /Users/mahir/Desktop/Agents/Application/TSD.docx. Do not ask for the code but the document itself.",
        max_consecutive_auto_reply=2,
        function_map={
            "get_section_mapping_and_upload_file": get_section_mapping_and_upload_file,
            "check_status_and_download_docx": check_status_and_download_docx,
        }
    )

    user_proxy.initiate_chat(TSD_bot, message=f"Generate the TSD and download it. Use the parameters given user_id: {user_id}, tsd_type: {tsd_type}, WRICEF_type: {WRICEF_type}, input_file_path: {input_file_path}.")

    data = extract_text("/Users/mahir/Desktop/Agents/Application/TSD.docx")
    return data

    # return "Success!"

def simulate_user_input():
    time.sleep(5)  # Give yourself a few seconds to focus the terminal
    pyautogui.typewrite("Check the status and download the docx file using check_status_and_download_docx function\n")

# result = TSDGenerator('Mahir.Jain1@ibm.com', 'Initial', 'report', 'FS RDD0304 - QM _Batch Genealogy Report V1.0 report.docx')
# print("Here the result: ", result)

# st.title("TSD Generator")

# user_id = st.text_input("User ID", "Mahir.Jain1@ibm.com")
# tsd_type = st.selectbox("TSD Type", ["Initial", "Final"])
# wricef_type = st.selectbox("WRICEF Type", ["Report", "Enhancement", "Interface"])
# input_file_path = st.text_input("Input File Path", "FS RDD0304 - QM _Batch Genealogy Report V1.0 report.docx")

# if st.button("Generate TSD"):
#     simulate_user_input()  # Simulate user input
#     result = TSDGenerator(user_id, tsd_type, wricef_type, input_file_path)
#     st.success(result)
#     if result == "Success!":
#         with open("/Users/mahir/Desktop/Agents/Application/TSD.docx", "rb") as file:
#             st.download_button(
#                 label="Download TSD",
#                 data=file,
#                 file_name="TSD.docx",
#                 mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#             )
