import warnings
from Code.IntraCodeAgent import codeOutputCheck
from TSD.TSDAgent import IntraAgent, user_proxy
from LLMConfig import llm_config_fsd, llm_config_coder, llm_config
from autogen import UserProxyAgent, AssistantAgent, GroupChatManager, GroupChat

warnings.filterwarnings("ignore")



tasks = [
    """Please generate the TSD using the parameters, that are user_id = 'Mahir.Jain1@ibm.com', tsd_type = 'Initial', WRICEF_type = 'Report', input_file_path = "FS RDD0304 - QM _Batch Genealogy Report V1.0 report.docx". After generation verify the TSD using testing function and Testing Agent as well. """,
    """After verification of TSD, reuse this TSD with WRICEF_type = 'Report', generate its ABAP code and also validate it.""",
]


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
