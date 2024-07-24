from TSD.TSDGenerator import TSDGenerator
from TSD.testingTSD import testing
from TSD.scraping import verification_Scraping
from TSD.LLMConfig_tsd import llm_config_intra_agent
from autogen import ConversableAgent

IntraAgent = ConversableAgent(
    name="IntraAgent",
    system_message="Download the TSD (Techincal Specification Document) by using the TSDGenerator function. Use the parameters given in the message. Then return the list of parameters that the generated TSD is failing at, by using the testing function. Reply TERMINATE when your task is done",
    llm_config=llm_config_intra_agent
)

# TestingAgent = AssistantAgent(
#     name="IntraScrapingAgent",
#     system_message="Verify the TSD (Techincal Specification Document) by using the Scraping function and then return the list of parameters that the generated TSD is failing at. Use this URL : 'https://community.sap.com/t5/forums/searchpage/tab/message?q=TSD&collapse_discussion=true'. Reply TERMINATE when your task is done",
#     llm_config=llm_config_scraping_agent
# )


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



# user_proxy.initiate_chat(
#     IntraAgent, message= f"""Please generate the TSD using the parameters, that are user_id = 'Mahir.Jain1@ibm.com', tsd_type = 'Initial', WRICEF_type = 'Report', input_file_path = "FS RDD0304 - QM _Batch Genealogy Report V1.0 report.docx". 
#                         After generation verify the TSD using testing function. 
#                         """)


# # return the last message the expert received
# print(user_proxy.last_message()["content"])