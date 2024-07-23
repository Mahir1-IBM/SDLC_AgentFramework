from LLMConfig import llm_config
from ibm_docx_parser import extract_text
from typing_extensions import Annotated
from autogen import ConversableAgent, AssistantAgent


def testing(
        data : Annotated[str, "TSD data that needs to be verified."],
        number: Annotated[int, "The index of the document"]
    ) -> tuple:

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
    return {number, user_proxy.last_message()["content"]}
    


# data = extract_text("/Users/mahir/Desktop/Agents/Application/TSD.docx")
# result = testing(data)

# print("Here's the result ", result)