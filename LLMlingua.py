import warnings
import os
from ibm_docx_parser import extract_text
from TSDGenerator import TSDGenerator
from testingTSD import testing
from dotenv import load_dotenv
import agentops

from autogen.agentchat.contrib.capabilities import transform_messages
from autogen.agentchat.contrib.capabilities.text_compressors import LLMLingua
from autogen.agentchat.contrib.capabilities.transforms import TextMessageCompressor
from autogen import ConversableAgent, config_list_from_json, UserProxyAgent

# Load environment variables
load_dotenv()

# Initialize AgentOps
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
if not AGENTOPS_API_KEY:
    raise ValueError("AGENTOPS_API_KEY not found in environment variables")

agentops.init(AGENTOPS_API_KEY)

warnings.filterwarnings("ignore")

@agentops.record_function('main')
def main():
    config_list = config_list_from_json(
        env_or_file = "OAI_CONFIG_LIST.json"
    )

    llm_config = {
        "config_list" : config_list, 
        "timeout" : 120
    }

    @agentops.record_function('extract_text')
    def extract_text_from_doc():
        return extract_text("/Users/mahir/Desktop/Agents/Application/TSD.docx")

    data = extract_text_from_doc()
    pdf_text = data

    @agentops.record_function('compress_text')
    def compress_text(text):
        llm_lingua = LLMLingua()
        text_compressor = TextMessageCompressor(text_compressor=llm_lingua)
        return text_compressor.apply_transform([{"content": text}])

    compressed_text = compress_text(pdf_text)

    @agentops.record_function('create_developer_agent')
    def create_developer_agent():
        developer = ConversableAgent(
            "assistant",
            llm_config={"config_list": config_list},
            max_consecutive_auto_reply=1,
            system_message = "You are a world class SAP developer that excels in creating a TSD.",
            human_input_mode="NEVER",
        )
        developer.register_for_llm(name="testing", description="For verification of the Techincal Specification Document (TSD). It returns a list of parmeters/filters which generated TSD lacked.")(testing)
        context_handling = transform_messages.TransformMessages(transforms=[TextMessageCompressor(text_compressor=LLMLingua())])
        context_handling.add_to_agent(developer)
        return developer

    @agentops.record_function('create_user_proxy_agent')
    def create_user_proxy_agent():
        user_proxy = UserProxyAgent(
            name = "user_proxy",
            system_message="You are a human admin, obtain a list from the developer and store it locally in a text file.",
            human_input_mode="NEVER",
            code_execution_config={
                "work_dir": "coding",
                "use_docker": False,
            },
            max_consecutive_auto_reply=1,
        )
        user_proxy.register_for_execution(name="testing")(testing)
        return user_proxy

    developer = create_developer_agent()
    user_proxy = create_user_proxy_agent()

    print("///////////////////////////////////////////////////////////////////////////////////////////////")
    print(compressed_text)
    print("///////////////////////////////////////////////////////////////////////////////////////////////")

    @agentops.record_function('initiate_chat')
    def initiate_chat():
        message = "Verify this text using the testing function : " + str(compressed_text)
        return user_proxy.initiate_chat(recipient=developer, clear_history=True, message=message, silent=True)

    result = initiate_chat()
    print("Chat Result:", result)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        agentops.log_error(str(e))
    finally:
        agentops.end_session('Success')