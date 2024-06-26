from typing_extensions import Annotated
from TSDGenerator import TSDGenerator
from autogen import ConversableAgent, config_list_from_json, AssistantAgent

config_list = config_list_from_json(
    env_or_file = "OAI_CONFIG_LIST.json"
)

llm_config = {
    "config_list" : config_list, 
    "timeout" : 120
}


def testing(
        data : Annotated[str, "TSD data that needs to be verified."],
    ) -> str:
    Tester = AssistantAgent(
        name="Agent_to_verify_TSD",
        system_message=f"""You are a very skilled AI agent. Check the {data} generated with the following parameters:
            1. Check for Description and Purpose Section, content should be available within this section.
            2. Check for Existing Assumptions, content should be available within this section.
            3. Check for Selection Screen, content should be available within this section.
            4. Check for Technical Details sections, within this section you should check for below things:
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
            5. Check for Error Handling section, content should be available within this section.
            6. Check for Security Requirements/Authorization Details section, content should be available within this section.
            7. Check for EXISTING Unit Test Plan section, content should be available within this section.
            8. Check for Interactive Report/Fiori/UI5 Application Flow section, content should be available within this section.
            9. Check for General Information,  within this section you should check for below things:
                - WRICEF ID, Description, Process owner, TS System Date, Module
            
           
            When the verification is done return 'TERMINATE'. 
            """,
        llm_config=llm_config,
    )

    user_proxy = ConversableAgent(
        name="user_proxy",
        human_input_mode="TERMINATE",
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False,
        max_consecutive_auto_reply = 3,
    )

    user_proxy.initiate_chat(
        Tester, message="Read the generated TSD and then verify it by given parameters. Return the parameters which were not satisfied by the TSD.")
    
    user_proxy.stop_reply_at_receive(Tester)
    user_proxy.send(
        "Give me a list of parameter that the generated result did not verify, return ONLY the list", Tester)

    # return the last message the expert received
    return user_proxy.last_message()["content"]
    

llm_config_intra_agent = {
    "functions": [
        {
            "name": "TSDGenerator",
            "description": "Function for generating the Techincal Specification Document (TSD). It returns the generated TSD as text"
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
        },
    ],
    "config_list": config_list
}


IntraAgent = ConversableAgent(
    name="IntraAgent",
    system_message="Download the TSD (Techincal Specification Document) by using the TSDGenerator function. Then return the list of parameters that the generated TSD is failing at, by using the testing function.Reply TERMINATE when your task is done",
    llm_config=llm_config_intra_agent
)

user_proxy = ConversableAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    function_map={
        "TSDGenerator": TSDGenerator,
        "testing": testing,
    }
)

user_proxy.initiate_chat(
    IntraAgent, message= f"Generate the TSD and verify it.")

