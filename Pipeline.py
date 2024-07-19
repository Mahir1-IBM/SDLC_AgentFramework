import warnings
from Code.IntraCodeAgent import codeOutputCheck
from TSD.TSDGenerator import TSDGenerator
from FSD.FSDvalidation import testingFSD
from TSD.TSDAgent import IntraAgent
from TSD.testingTSD import testing
from autogen import UserProxyAgent, config_list_from_json, AssistantAgent, GroupChatManager, GroupChat, ConversableAgent

warnings.filterwarnings("ignore")

config_list = config_list_from_json(
    env_or_file = "OAI_CONFIG_LIST.json"
)

llm_config = {
    "config_list" : config_list, 
    "timeout" : 120
}


llm_config_fsd = {
    "functions": [
        {
            "name": "testingFSD",
            "description": "For verification of the Functional Specification Document (FSD). It returns a list of parmeters/filters which input FSD fails to staisfy",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "string",
                            "description": "FSD data that needs to be verified. FSD will be input by user",
                        },
                    },
                "required": ["data"],
            },
        },
    ],
    "config_list": config_list

}

llm_config_coder = {
    "functions": [
        {
            "name": "codeOutputCheck",
            "description": "Generates the SAP ABAP Code using the TSD and also validates the code produced.",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "WRICEF_type": {
                            "type": "string",
                            "description": "The type of WRICEF of TSD : Reports or Enhancements or Interfaces.",
                        },
                    },
                "required": ["WRICEF_type"],
            },
        },
    ],
    "config_list": config_list
}


tasks = [
    """Please generate the TSD using the parameters, that are user_id = 'Mahir.Jain1@ibm.com', tsd_type = 'Initial', WRICEF_type = 'Report', input_file_path = "FS RDD0304 - QM _Batch Genealogy Report V1.0 report.docx". After generation verify the TSD using testing function and Testing Agent as well. """,
    """After verification of TSD, reuse this TSD with WRICEF_type = 'Report', generate its ABAP code and also validate it.""",
]


user_proxy = ConversableAgent(
    name="user_proxy_main",
    system_message="Use the parameters given and send them to the IntraAgent to be used to generate the TSD. Get the list of parameters which are not satisfied by TSD, use testing funciton.",
    human_input_mode="NEVER",
    max_consecutive_auto_reply= 4,
    function_map={
        "TSDGenerator": TSDGenerator,
        "testing": testing,
    }
)


groupchat = GroupChat(
    agents=[user_proxy, IntraAgent],
    messages=[],
    speaker_selection_method='round_robin',
    allow_repeat_speaker=False,
)

manager = GroupChatManager(
    groupchat=groupchat,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=llm_config
)


Coder = AssistantAgent(
    name="Coder",
    system_message="You are a skilled SAP coder, and using the TSD generate its corresponding ABAP code by using the codeOutputCheck function. Return 'TERMINATE' after completion of the work. ",
    llm_config=llm_config_coder
)

FSDValidator = AssistantAgent(
    name="FSDValidator",
    system_message="Use the input FSD and validate it using the given checklist. This FSD will be later used for TSD generation.(SLDC)",
    llm_config=llm_config_coder
)


user = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    # is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    function_map={
        "codeOutputCheck": codeOutputCheck,
    },
    code_execution_config={
        "work_dir": "tasks",
        "use_docker": False,
    }, 
)


res = user.initiate_chats(
    [
        {"recipient": manager, "message": tasks[0], "summary_method": "reflection_with_llm"},
        {"recipient": Coder, "message": tasks[1]},
    ]
)
