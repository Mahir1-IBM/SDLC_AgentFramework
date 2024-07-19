from typing import Annotated
from autogen import ConversableAgent
from Code.CodeGeneration import CodeGenAPI
from Code.CodeValidation import testingCode
from LLMConfig import llm_config_code_agent


def codeOutputCheck(
        WRICEF_type: Annotated[str, "The wricef type of the TSD."],
    ) -> str:
    
    IntraAgent = ConversableAgent(
        name="IntraAgent",
        system_message="Generate the SAP ABAP code from the given Techincal Specification Document by using the CodeGenAPI function. Then return the list of parameters that the generated code is failing at, by using the testingCode function. Reply TERMINATE when your task is done",
        llm_config=llm_config_code_agent
    )

    user_proxy = ConversableAgent(
        name="user_proxy",
        human_input_mode="TERMINATE",
        function_map={
            "CodeGenAPI": CodeGenAPI,
            "testingCode": testingCode,
        }
    )

    user_proxy.initiate_chat(
        IntraAgent, message= f"Generate and verify the ABAP code by the given TSD using the arguments : WRICEF_type = {WRICEF_type}; input_file_path = '/Users/mahir/Desktop/Agents/Application/TSD.docx'.")


    return (user_proxy.last_message()["content"])


# print(codeOutputCheck("Report"))