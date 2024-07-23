import os
from typing import Annotated
from ibm_docx_parser import extract_text
from autogen import GroupChatManager, AssistantAgent, UserProxyAgent, GroupChat, ConversableAgent
from LLMConfig import llm_config, llm_config_test, llm_config_test_2, llm_config_generator

default_path = "/Users/mahir/Desktop/Agents/Application/codeimprovment/"

def ReadingDocx(
    path: Annotated[str, "Name and path of file to change."],
)-> str:
    data = extract_text(path)

    return data

def create_file(
    filename: Annotated[str, "Name and path of file to create."], text: Annotated[str, "Text to write in the file."]
):
    with open(default_path + filename, "w") as file:
        file.write(text)
    return 0, "File created successfully"

def split_document(text):
    # Find the start and end of the Technical Details section
    tech_details_start = text.find("**Technical Details**")
    tech_details_end = text.find("**", tech_details_start + 20)  # Look for the next section after Technical Details

    if tech_details_start == -1 or tech_details_end == -1:
        print("Could not find the Technical Details section.")
        return None, None, None

    # Split the document
    part1 = text[:tech_details_start].strip()
    part2 = text[tech_details_start:tech_details_end].strip()
    part3 = text[tech_details_end:].strip()

    return part1, part2, part3

def generating(
        Data: Annotated[str, "Previous TSD text"],
        number: Annotated[int, "The index of the document"],
        params : Annotated[str, "Parameters that previous TSD couldnt satisfy"],
) -> tuple:
    
    # part1, part2, part3 = split_document(Data)

    generator = AssistantAgent(
        name="Agent_for_TSD",
        system_message=f"""You are a very skilled AI agent. The previous TSD is {Data}, Check it out and then using the {params}, create a similar TSD with same format as that of previous TSD.
                            Do not add any extra headings or sub headings.
                            When the verification is done return 'TERMINATE'. 
            """,
        llm_config=llm_config,
    )

    user_proxy = ConversableAgent(
        name="user_proxy_generatorTSD",
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False,
        max_consecutive_auto_reply = 2,
    )

    user_proxy.initiate_chat(
        generator, message="Read the generated TSD and then generate another one that verifies the given parameters. Return the newly generated TSD.")
    
    user_proxy.stop_reply_at_receive(generator)
    user_proxy.send(
        "Make sure that the TSD generated is in same format as the previous ones. Give me the final text.", generator)

    # return the last message the expert received
    return {number, user_proxy.last_message()["content"]}
    