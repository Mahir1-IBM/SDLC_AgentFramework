import time
import asyncio
import warnings
import streamlit as st

from LLMConfig import llm_config_intra_agent
from ibm_docx_parser import extract_text
from TSD.TSDGenerator import TSDGenerator, simulate_user_input
from TSD.testingTSD import testing
from FSD.FSDvalidation import testingFSD
from autogen import ConversableAgent

warnings.filterwarnings("ignore")


st.set_page_config(page_title="Agent Framework for SAP process", page_icon="🤖", layout="wide")

st.title("Intra Agent")

class TrackableAssistantAgent(ConversableAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            if isinstance(message, dict):
                st.json(message)
            else:
                st.markdown(message)
        return super()._process_received_message(message, sender, silent)

class TrackableUserProxyAgent(ConversableAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            if isinstance(message, dict):
                st.json(message)
            else:
                st.markdown(message)
        return super()._process_received_message(message, sender, silent)


st.sidebar.title("Input Details* (Required)")

# IBM ID input
ibm_id = st.sidebar.text_input("User ID")

# TSD type dropdown
tsd_type = st.sidebar.selectbox("TSD Type", ["Initial", "Final"])

# WRICEF type dropdown
wricef_type = st.sidebar.selectbox("WRICEF Type", ["REPORTS", "INTERFACES", "ENHANCEMENTS"])

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload a document file", type=["txt", "docx", "pdf"])

# Validate FSD button
validate_button = st.sidebar.button("Validate FSD")

# Generate TSD button
generate_button = st.sidebar.button("Generate TSD")


def validate_fsd(file):
    data = extract_text(file)
    results = testingFSD(data)
    return results

with st.container():

    if validate_button and uploaded_file:
        with st.spinner("Validating FSD..."):
            time.sleep(1) 
            validation_result = validate_fsd(uploaded_file)
            st.write("FSD Validation Result:", validation_result)
    
    if generate_button:
        if not ibm_id:
            st.error("Please enter your IBM ID.")
        elif not uploaded_file:
            st.error("Please upload a document file.")
        else:
            st.empty()
            

            # assistant = TrackableAssistantAgent(
            #     name="IntraAgent",
            #     system_message="Download the TSD (Techincal Specification Document) by using the TSDGenerator function. Use the parameters given in the message. Then return the list of parameters that the generated TSD is failing at, by using the testing function. Reply TERMINATE when your task is done",
            #     llm_config=llm_config_intra_agent
            # )

            # user_proxy = TrackableUserProxyAgent(
            #     name="user",
            #     system_message="Use the parameters given and send them to the IntraAgent to be used to generate the TSD. Get the list of parameters which are not satisfied by TSD, use testing function",
            #     human_input_mode="NEVER",
            #     is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
            #     function_map={
            #         "TSDGenerator": TSDGenerator,
            #         "testing": testing,
            #     }
            # )

            # loop = asyncio.new_event_loop()
            # asyncio.set_event_loop(loop)

            # async def initiate_chat():
            #     await user_proxy.a_initiate_chat(assistant, message=f"Generate the TSD using the parameters: user_id = {ibm_id}, tsd_type = {tsd_type}, WRICEF_type = {wricef_type}, input_file_path = 'FS RDD0304 - QM _Batch Genealogy Report V1.0 report.docx'. After generation verify the TSD using testing function.")

            # loop.run_until_complete(initiate_chat())

 
st.stop()
