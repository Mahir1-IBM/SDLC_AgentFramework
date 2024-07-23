import os
from typing import Annotated
from ibm_docx_parser import extract_text
from autogen import GroupChatManager, AssistantAgent, UserProxyAgent, GroupChat, ConversableAgent
from TSDCorrection.testingTSD import testing
from TSDCorrection.Functions import generating, ReadingDocx, create_file
from LLMConfig import llm_config, llm_config_test, llm_config_test_2, llm_config_generator

default_path = "/Users/mahir/Desktop/Agents/Application/codeimprovment/"


# reader = AssistantAgent(
#     name="Reader",
#     llm_config=llm_config_test,
#     system_message="""
#     I'm SAP Engineer. I'm expert in reading Technical Specification Documents (TSD) and I know that this document would be used to generate ABAP code, in the SDLC.
#     """,
# )

tester = AssistantAgent(
    name="Tester",
    llm_config=llm_config_test_2,
    system_message="""
    You're a SAP Engineer. You're expert in analysing Technical Specification Documents (TSD). 
    You will return a list of parameters using the testing function, and then pass it to the generator.
    After 3 rounds of content iteration, add TERMINATE to the end of the message",
    """,
)

generator = AssistantAgent(
    name="Generator",
    llm_config=llm_config_generator,
    system_message="""
    You're a SAP Engineer. You're expert in creating Technical Specification Documents (TSD) - SAP.
    You will generate a document - TSD aligning with parameters sent by the Tester, wait for its input to get a list of verification list, use that to call generating function.
    After 3 rounds of content iteration, add TERMINATE to the end of the message",
    """,
)

user_proxy_bhaiya = UserProxyAgent(
    name="UserBhaiya",
    human_input_mode="NEVER",
    code_execution_config=False, 
    system_message="Interact with generator and tester, ask generator to create new TSD and tester to verfiy it. Do this multiple times",
    function_map={
        "testing" : testing,
        "generating" : generating
    },
)

user_proxy = UserProxyAgent(
    name="Admin",
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": "tasks",
        "use_docker": False,
    }, 
    system_message="Interact with Engineer to helo with its task. Use tools",
    function_map={
        "ReadingDocx": ReadingDocx,
        "create_file" : create_file,
    },
)

groupchat = GroupChat(
    agents=[user_proxy_bhaiya, tester, generator],
    messages=[],
    max_round=500,
)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

def get_file_path():
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, "TSD.docx")
    return file_path


params = """
        Here is a list of parameters that the generated Technical Specification Document (TSD) did not verify, along with a detailed explanation of each point:

        1. **Existing Assumptions:**
        - **Explanation:** The TSD mentions "NA" for this section. Ideally, if there are no existing assumptions, the document should explicitly state "No existing assumptions." This provides clarity that the absence of assumptions is confirmed rather than overlooked.

        2. **Selection Screen:**
        - **Explanation:** The section is marked as "NA." The TSD should clarify whether a selection screen is not required or provide detailed specifications if it is required. This ensures that the developers are aware of all user input requirements for generating the report.

        3. **Technical Details - Function Names and Class Names:**
        - **Explanation:** The TSD does not list specific ABAP function names or class names that would be implemented or used in the report. Providing this information is critical for developers to understand which reusable components or new classes/functions will be involved in the solution.

        4. **Technical Details - Important Functionalities:**
        - **Explanation:** The TSD lacks a detailed description of important functionalities that the report should include. For instance, it should specify error checking, data validation, and any specific business logic that needs to be implemented.

        5. **Technical Details - Separate Section for Enhancements:**
        - **Explanation:** There is no separate section that outlines potential enhancements or future scalability considerations. This section is important to foresee potential growth or additional features that might be required later.

        6. **Technical Details - Pseudo Codes in Tables:**
        - **Explanation:** The TSD does not provide pseudo-codes or example table structures. Pseudo-codes help in understanding the essential logic flow before actual coding begins, making it easier to align with business requirements.

        7. **Error Handling Section:**
        - **Explanation:** The section is labeled "NA," which is insufficient. Error handling details are crucial for any technical document to prepare for and manage unexpected scenarios and ensure the robustness of the solution.

        8. **Security Requirements/Authorization Details Section:**
        - **Explanation:** Labeled as "NA" with no further explanation. This section should detail the security requirements and authorization checks necessary to ensure that only authorized personnel can access or run the report.

        9. **EXISTING Unit Test Plan Section:**
        - **Explanation:** This section is incomplete or missing. A unit test plan is essential to verify that each unit of the software performs as designed. It ensures that individual parts of the application are working correctly.

        10. **Interactive Report/Fiori/UI5 Application Flow Section:**
            - **Explanation:** Marked as "NA," indicating that this section was either overlooked or deemed not necessary. If the report integrates with an interactive interface or Fiori/UI5 applications, details on the application flow are essential for implementation and user experience.

        11. **General Information - Process Owner:**
            - **Explanation:** The process owner information is missing. Identifying the process owner is important as it indicates who is responsible for the process and who can provide further clarifications or approvals.
    """



tasks = [
    f""" Check out the TSD docx file using the {get_file_path()} """,
    f"""You will need to improve the TSD according to {params}, try to read it and then change it so that new TSD docx follows the parameters.""",
]


# chat_result = user_proxy.initiate_chats(
#     [
#         {"recipient": reader, "message": tasks[0], "summary_method": "reflection_with_llm"},
#         {"recipient": manager, "message": tasks[1]},
#     ]
# )

# print(get_file_path())


data = extract_text("/Users/mahir/Desktop/Agents/Application/TSD.docx")
print(data)