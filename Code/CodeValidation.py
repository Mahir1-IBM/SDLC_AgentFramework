from typing_extensions import Annotated
from LLMConfig import llm_config
from autogen import ConversableAgent, AssistantAgent

async def testingCode(
        code : Annotated[str, "code in json format that needs to be verified."],
    ) -> str:
    CodeTester = AssistantAgent(
        name="Agent_to_verify_ABAP_code",
        system_message=f"""You are expert SAP ABAP Programmer, Your task is to decompose a set of SAP ABAP code and verify that the code must be well-defined and following these parameters given below : .
        
        Here is the SAP ABAP code : {code}, verify if it follows these guidelines :               
            1. Object-Oriented Formatting:
                Check if the code follows object-oriented principles, including class definitions, method implementations, and appropriate use of inheritance and polymorphism.
            
            2. Syntax and Logic:
                Verify the syntax of the ABAP code for correctness.
                Ensure the logical flow of the program is correct and aligns with the requirements.
            
            3.User Input Handling:
                Confirm that selection screens are used for user input only if explicitly mentioned in the requirement.
                Validate input to maintain data integrity.
            
            4. Utilization of SAP BAPI:
                Ensure the code uses standard SAP BAPI function modules wherever applicable.
            
            5. Use of Standard SAP Tables:
                Verify the code uses standard SAP tables unless custom tables are explicitly specified in the requirement.
            
            6. Custom Function Definitions:
                If custom functions are used, ensure their definitions are provided within the generated code.
            
            7. Requirement Adherence:
                Check that all requirements specified are addressed in the code without skipping any.
            
            8. Error Handling:
                Ensure proper error handling mechanisms are implemented in the code.
            
            9. SAP Coding Standards:
                Verify adherence to SAP’s recommended coding standards and best practices.
            
            10. No Explanations in Code:
                Confirm that no explanations are provided within the code comments.
                
            When the verification is done return 'TERMINATE'. 
            """,
        llm_config=llm_config,
    )

    user_proxy = ConversableAgent(
        name="user_proxy_val",
        system_message='''You are a human proxy. Make sure that the CodeTester verifies SAP ABAP code, from the given business requirement. Do not generate any code in your response. Make sure it returns a list''',
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False,
        max_consecutive_auto_reply = 1,
    )

    user_proxy.initiate_chat(
        CodeTester, message = f"Read the SAB ABAP generated code: {code} and then verify it by given parameters. Return the parameters which were not satisfied by the ABAP code. Strictly Ensure you will cover each and everything from the SAP ABAP code requirements into the output JSON , nothing should be missed from detailed technical approaches and implementation steps, technical details.")
    
    user_proxy.stop_reply_at_receive(CodeTester)
    user_proxy.send(
        "Give me a list of points that the generated result do not have, with a proper explaination of each point.", CodeTester)

    return user_proxy.last_message()["content"]
    

# code = CodeGenAPI("Enhancement", "/Users/mahir/Desktop/Agents/Application/CodeGen/O2C_E_826_827_Product Allocation UK_TDS.docx")
# print(testingCode(code))