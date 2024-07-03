import warnings

from typing_extensions import Annotated
from ibm_docx_parser import extract_text
from autogen import ConversableAgent, config_list_from_json, AssistantAgent
warnings.filterwarnings("ignore")

config_list = config_list_from_json(
    env_or_file = "OAI_CONFIG_LIST.json"
)

llm_config = {
    "config_list" : config_list, 
    "timeout" : 120
}

def testingFSD(
        data : Annotated[str, "FSD data that needs to be verified."],
    ) -> str:
    Tester = AssistantAgent(
        name="Agent_to_verify_FSD",
        system_message=f"""Here is the FSD : {data}, verify if it follows the rules : 
                A functional specification document is like a roadmap for building software. It breaks down what the software should do and how. 
                Introduction: Explain the main reason for the project. What problem does it aim to solve, or what new capabilities will it offer? Briefly describe the intended audience for this software.
                Scope: Define what’s included in the project, and clearly state any items or areas that will not be addressed in this phase.
                Objectives: List the specific, measurable targets for the project. Describe the results that will indicate success, and ensure they align with broader business needs.
                Functional requirements: Describe, in detail, each specific action or task the software must enable users to perform. Include the expected response or outcome from the system for each function.
                Non-functional requirements: Describe the practical requirements of the software: how fast it should respond, what security measures are required, how user-friendly it should be, whether it needs to be upgraded in the work or.
                User stories or use cases: Define the performance standards, security protocols, desired level of user-friendliness, and the ability to handle updates seamlessly.
                Wireframes or mockups: Include detailed sketches, diagrams, or mockups to illustrate the proposed layout, product routing, and overall design aesthetic of the user interface.
                Acceptance criteria: Set up clear and verifiable criteria for determining whether the software meets the defined requirements and stakeholder expectations.
                Assumptions and constraints: List any assumptions that might affect the project plan related to technology or resources availability. Identify any potential factors that may limit or influence the project’s execution (e.g., budget, timeline, external dependencies).
            
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
        "Give me a list of parameter that the generated result did not verify, with a proper explaination of each point.", Tester)

    # return the last message the expert received
    return user_proxy.last_message()["content"]
    
# data = extract_text("/Users/mahir/Desktop/Agents/Application/FS RDD0304 - QM _Batch Genealogy Report V1.0 report.docx")
# print(testingFSD(data))