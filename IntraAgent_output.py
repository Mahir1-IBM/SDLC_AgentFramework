import warnings

from TSDGenerator import TSDGenerator
from testingTSD import testing
from autogen import ConversableAgent, config_list_from_json, AssistantAgent, GroupChat, GroupChatManager


warnings.filterwarnings("ignore")

config_list = config_list_from_json(
    env_or_file = "OAI_CONFIG_LIST.json"
)

llm_config = {
    "config_list" : config_list, 
    "timeout" : 120
}

llm_config_scraping_agent = {
    "functions": [
        {
            "name": "research",
            "description": "For verification of the Techincal Specification Document (TSD). It returns a list of parmeters/filters which generated TSD lacked",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "string",
                            "description": "Website that should be scraped to get information and parameters for TSD.",
                        },
                    },
                "required": ["url"],
            },
        },
    ],
    "config_list": config_list
}


llm_config_intra_agent = {
    "functions": [
        {
            "name": "TSDGenerator",
            "description": "Function for generating the Techincal Specification Document (TSD). It returns the generated TSD as text",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user id of the user.",
                        },
                        "tsd_type": {
                            "type": "string",
                            "description": "The type of TSD to be generated : initial or final.",
                        },
                        "WRICEF_type": {
                            "type": "string",
                            "description": "The type of WRICEF to be used : Reports or Enhancements or Interfaces.",
                        },
                        "input_file_path": {
                            "type": "string",
                            "description": "The path where FSD is stored.",
                        },
                    },
                "required": ["user_id", "tsd_type", "WRICEF_type", "input_file_path"],
            },
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
    system_message="Download the TSD (Techincal Specification Document) by using the TSDGenerator function. Use the parameters given in the message. Then return the list of parameters that the generated TSD is failing at, by using the testing function.Reply TERMINATE when your task is done",
    # system_message="Download the TSD (Techincal Specification Document) by using the TSDGenerator function. Then return the list of parameters that the generated TSD is failing at, by using the testing function.Reply TERMINATE when your task is done",
    llm_config=llm_config_intra_agent
)

TestingAgent = AssistantAgent(
    name="IntraScrapingAgent",
    system_message="Verify the TSD (Techincal Specification Document) by using the Scraping function and then return the list of parameters that the generated TSD is failing at. Use this URL : 'https://community.sap.com/t5/forums/searchpage/tab/message?q=TSD&collapse_discussion=true'. Reply TERMINATE when your task is done",
    llm_config=llm_config_scraping_agent
)


user_proxy = ConversableAgent(
    name="user_proxy",
    system_message="Use the parameters given and send them to the IntraAgent to be used to generate the TSD. Get the list of parameters which are not satisfied by TSD, use testing funciton",
    max_consecutive_auto_reply= 2,
    human_input_mode="TERMINATE",
    function_map={
        "TSDGenerator": TSDGenerator,
        "testing": testing,
    }
)


# group_chat = GroupChat(
#     agents=[user_proxy, TestingAgent, IntraAgent], messages=[], max_round=12
# )
# manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)


user_proxy.initiate_chat(
    IntraAgent, message= f"Generate the TSD using the parameters, that are user_id = 'Mahir.Jain1@ibm.com', tsd_type = 'Initial', WRICEF_type = 'report', input_file_path = 'FS RDD0304 - QM _Batch Genealogy Report V1.0 report.docx'. After generation verify the TSD using testing function and Testing Agent as well.")

user_proxy.stop_reply_at_receive(IntraAgent)
user_proxy.send(
    "Here is the list of parameters that the TSD is following, verify it it is indeed following them or not.", TestingAgent)

# return the last message the expert received
print(user_proxy.last_message()["content"])