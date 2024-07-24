import os
from typing import Annotated
from ibm_docx_parser import extract_text
from autogen import GroupChatManager, AssistantAgent, UserProxyAgent, GroupChat, ConversableAgent
from LLMConfig import llm_config, llm_config_test, llm_config_test_2, llm_config_generator

default_path = "/Users/mahir/Desktop/Agents/Application/codeimprovment/"



# ///////////////////////////////////////////////// FOR READING THE DOCUMENTS //////////////////////////////////////////////////////
def ReadingDocx(
    path: Annotated[str, "Name and path of file to change."],
)-> str:
    data = extract_text(path)

    return data



# ///////////////////////////////////////////////// FOR CREATING AND SAVING THE DOCUMENT //////////////////////////////////////////////////////
def create_file(
    Path: Annotated[str, "Path of file to create."], 
    number: Annotated[int, "Name of file to create."], 
    text: Annotated[str, "Revised TSD text to be written in the file."]
):
    filename = f"Revised{number}.txt"
    with open(Path + filename, "w") as file:
        file.write(text)
    return 0, "File created successfully"



# ///////////////////////////////////////////////// FOR SPLITTING THE DOCUMENTS //////////////////////////////////////////////////////
def split_document(path):

    text = extract_text(path)
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



# ///////////////////////////////////////////////// FOR GENERATING THE MODULAR TSD //////////////////////////////////////////////////////
def generating(
        Data: Annotated[str, "Previous TSD text"],
        # number: Annotated[int, "The index of the document"],
        params : Annotated[str, "Parameters that previous TSD couldnt satisfy"],
) -> str:
    
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
    return user_proxy.last_message()["content"]



# ///////////////////////////////////////////////// FOR TESTING THE MODULAR TSD //////////////////////////////////////////////////////
def testing(
        data : Annotated[str, "TSD data that needs to be verified."],
        number: Annotated[int, "The index of the document"]
    ) -> str:

    # number = 3

    if number == 1:
        system_message = f"""You are a very skilled AI agent. Check the {data} generated with the following parameters:
            1. Check for Description and Purpose Section, content should be available within this section.
            2. Check for Existing Assumptions, content should be available within this section.
            3. Check for Selection Screen, content should be available within this section.
            When the verification is done return 'TERMINATE'."""
    
    elif number == 2:
        system_message = f"""You are a very skilled AI agent. Check the {data} generated with the following parameters:
            Check for Technical Details sections, within this section you should check for below things:
                - Main Statement of Reports
                - Key requirements
                - Relevant Data Fields
                - Data Sources
                - SAP Tools
                - Report output fields
                - Function names and class names
                - Important functionalities
                - Custom table design
                - Custom CDS Views, tables, classes, methods, and functions
                - Technical implementation steps.
                - Technical implementation steps should strictly exclude generic sections Error Handling, Testing, Selection screen, Documentation, Conclusion, etc
                - Separate section for enhancements
                - Pseudo Codes in Tables
            When the verification is done return 'TERMINATE'. """
   
    else : 
        system_message = f"""You are a very skilled AI agent. Check the {data} generated with the following parameters:
            Check for Security Requirements/Authorization Details section, content should be available within this section.
            7. Check for EXISTING Unit Test Plan section, content should be available within this section.
            8. Check for Interactive Report/Fiori/UI5 Application Flow section, content should be available within this section.
            9. Check for General Information,  within this section you should check for below things:
                - WRICEF ID, Description, Process owner, TS System Date, Module
            When the verification is done return 'TERMINATE'."""


    Tester = AssistantAgent(
        name="Agent_to_verify_TSD",
        system_message = system_message,
        llm_config=llm_config,
    )

    user_proxy = ConversableAgent(
        name="user_proxy_tester",
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False,
        max_consecutive_auto_reply = 1,
    )

    user_proxy.initiate_chat(
        Tester, message="Read the given text and thena verify it by given parameters. Return the parameters which were not satisfied by the text.")
    
    user_proxy.stop_reply_at_receive(Tester)
    user_proxy.send(
        "Give me a list of parameter that the generated text did not verify, with a proper explaination of each point.", Tester)

    # return the last message the expert received
    return user_proxy.last_message()["content"]
    



# ///////////////////////////////////////////////// split_document IMPLEMENTATION  //////////////////////////////////////////////////////

# part1, part2, part3 = split_document("/Users/mahir/Desktop/Agents/Application/TSD.docx")

# if part1 and part2 and part3:
#     with open('part1.txt', 'w') as file:
#         file.write(part1)
#     with open('part2.txt', 'w') as file:
#         file.write(part2)
#     with open('part3.txt', 'w') as file:
#         file.write(part3)
#     print("Document successfully split into three parts.")
# else:
#     print("Failed to split the document.")