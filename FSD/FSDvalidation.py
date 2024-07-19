from typing_extensions import Annotated
from autogen import ConversableAgent, AssistantAgent
from LLMConfig import llm_config

def testingFSD(
        data : Annotated[str, "FSD data that needs to be verified."],
    ) -> str:
    Tester = AssistantAgent(
        name="Agent_to_verify_FSD",
        system_message=f"""Here is the FSD : {data}, verify if it follows these rules :               
                "General Information": [
                    "General information",
                    "General Object Overview",
                    "Purpose of this document"
                ],
                "DESCRIPTION AND PURPOSE": [
                    "Process Requirements Reference",
                    "Purpose of this document",
                    "Business Benefit",
                    "Business Requirement & High-Level Process Flow",
                    "Justification",
                    "scope",
                    "Overview",
                    "Business Driver",
                    "DESCRIPTION AND PURPOSE"
                ],
                "ASSUMPTIONS": [
                    "Assumptions",
                    "Assumptions and Dependencies",
                    "Key Assumptions"
                ],
                "List of Custom_Developed Primary Object": [],
                "Selection Screen": [
                    "Selection Screen",
                    "Selection Criteria:"
                ],
                "Technical Details": [
                    "scope",
                    "Generic WRICEF Descriptions",
                    "Reporting (operational and analytical)",
                    "Development Description",
                    "FUNCTIONAL DESCRIPTION / DESIGN",
                    "Object Specific Design",
                    "Report Fields",
                    "Report Output/Display",
                    "Customs Table for Customs Duty - ZOTC_CUSTOMSDUTY"
                ],
                "Interactive Report/Fiori/UI5 Application Flow": [
                    "Flow of Screens/Logic/Data"
                ],
                "Calculations and Page Break Related Information": [
                    "Report Structure & Sorting"
                ],
                "Error Handling": [
                    "Error Handling"
                ],
                "Security Requirements/Authorization Details": [
                    "AUTHORIZATION REQUIREMENTS",
                    "Security & Authorization",
                    "Security Requirements "
                ],
                "Additional Information and Attachments": [
                    "Alternate Solutions Evaluated"
                ],
                "Unit Test Plan": [
                    "Testing Scenarios",
                    "Functional Test Cases",
                    "Test Conditions",
                    "Reporting (operational and analytical)"
                ]
            Check these headings which are the keys and check for the sub headings that are the values.
            When the verification is done return 'TERMINATE'. 
            """,
        llm_config=llm_config,
    )

    user_proxy = ConversableAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False,
        max_consecutive_auto_reply = 1,
    )

    user_proxy.initiate_chat(
        Tester, message = f"Read the FSD: {data} and thena verify it by given parameters. Return the parameters which were not satisfied by the FSD.")
    
    user_proxy.stop_reply_at_receive(Tester)
    user_proxy.send(
        "Give me a list of headings and sub headings that the generated result do not have, with a proper explaination of each point.", Tester)

    # return the last message the expert received
    return user_proxy.last_message()["content"]
    
# data = extract_text("/Users/mahir/Desktop/Agents/Application/FS RDD0304 - QM _Batch Genealogy Report V1.0 report.docx")
# print(testingFSD(data))