import os
from typing import Annotated
from ibm_docx_parser import extract_text
from autogen import GroupChatManager, AssistantAgent, UserProxyAgent, GroupChat, ConversableAgent
from TSDCorrection.Functions import generating, ReadingDocx, create_file, testing, split_document
from LLMConfig import llm_config, llm_config_test, llm_config_test_2, llm_config_generator, llm_config_split, llm_config_saver

default_path = "/Users/mahir/Desktop/Agents/Application/codeimprovment/"

def get_file_path():
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, "TSD.docx")
    return file_path

    
def CorrectionInParts(
        UserProxy : Annotated[object, "Agent to initiate chats"],
        number: Annotated[int, "Index of parameter to be used for verification."],
        data : Annotated[str, "TSD text data"], 
):
    tasks = [f"""You will need to improve the TSD : {data}, try to read it and then change it so that new TSD docx follows the parameters. Pass on the new revised TSD generated. After changing make sure to save it to a text file."""]

    tester = AssistantAgent(
        name="Tester",
        llm_config=llm_config_test_2,
        system_message= f"""
        You're a SAP Engineer. You're expert in analysing Technical Specification Documents (TSD). 
        Analyse the TSD received by the generator then return a list of parameters using the testing function, and then pass it to the generator.
        Always use the number = {number} when using the testing function.
        Do not change the TSD obtained.
        After 2 rounds of content iteration, save the TSD text in a file using create_file function. Add TERMINATE to the end of the message after completion",
        """,
    )

    generator = AssistantAgent(
        name="Generator",
        llm_config=llm_config_generator,
        system_message="""
        You're a SAP Engineer. You're expert in creating Technical Specification Documents (TSD) - SAP.
        Take input a text and a list of parameters. 
        You will generate a document - TSD aligning with parameters sent by the Tester, wait for the verification list and use that to call generating function.
        After 2 rounds of content iteration, add TERMINATE to the end of the message after completion",
        """,
    )

    saver = AssistantAgent(
        name="Saver",
        llm_config=llm_config_saver,
        system_message=f"""
            After obtaining the new TSD text, save it using create_file function.
            Path = '/Users/mahir/Desktop/Agents/Application/TSDCorrection' and number = {number}, create a file.
            Do not execute any code, only use the create_file function.
        """,
    )

    user_proxy_bhaiya = UserProxyAgent(
        name="UserBhaiya",
        human_input_mode="NEVER",
        code_execution_config=False, 
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        # max_consecutive_auto_reply = 12,
        system_message= f"""Interact with generator and tester, ask generator to create new TSD using the parameters provided and tester to verfiy it. Do this multiple times. 
        Always use the number = {number} when using the testing function.
        Make sure to provide the revised TSD text to saver for saving it in a text file.
        """,
        function_map={
            "generating" : generating,
            "testing" : testing,
            "create_file" : create_file
        },
    )

    # def state_transition(last_speaker, groupchat):

    #     if last_speaker is user_proxy_bhaiya:
    #         return generator
    #     elif last_speaker is generator:
    #         return tester
    #     elif last_speaker is tester:
    #         return user_proxy_bhaiya

    groupchat = GroupChat(
        agents=[user_proxy_bhaiya, tester, generator],
        messages=[],
        speaker_selection_method="round_robin",
        max_round=15,
    )
    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    chat_result = UserProxy.initiate_chats(
        [
            {"recipient": manager, "message": tasks[0], "summary_method": "last_msg"},
            # {"recipient": saver, "message": tasks[1]},
        ]
    )

    return chat_result



user_proxy = UserProxyAgent(
    name="Admin",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "tasks",
        "use_docker": False,
    }, 
    system_message="Interact as a human admin.",
    function_map={
        "ReadingDocx": ReadingDocx,
        "split_document" : split_document,
        "create_file" : create_file,
    },
)

splitter = AssistantAgent(
    name="Splitter",
    llm_config=llm_config_split,
    system_message= "Split a document given by its path. Use split_document function. Return 'TERMINATE' after the task is completed.",
)


with open("TSDCorrection/part1.txt", "r") as file:
    data = file.read().replace("\n", "")

CorrectionInParts(user_proxy, 1, data)

# tasks = ["Split the TSD into three parts, path = '/Users/mahir/Desktop/Agents/Application/TSD.docx.' ", 
#         ""
# ]

# chat_result = user_proxy.initiate_chats(
#     [
#         {"recipient": splitter, "message": tasks[0], "summary_method": "reflection_with_llm"},
#         {"recipient": manager, "message": tasks[0]},
#     ]
# )
