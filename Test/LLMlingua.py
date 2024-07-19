from ibm_docx_parser import extract_text
from TSD.testingTSD import testing
from dotenv import load_dotenv

from LLMConfig import llm_config
from autogen.agentchat.contrib.capabilities import transform_messages
from autogen.agentchat.contrib.capabilities.text_compressors import LLMLingua
from autogen.agentchat.contrib.capabilities.transforms import TextMessageCompressor
from autogen import ConversableAgent, config_list_from_json, UserProxyAgent

load_dotenv()

data = extract_text("/Users/mahir/Desktop/Agents/Application/TSD.docx")

pdf_text = data

llm_lingua = LLMLingua()
text_compressor = TextMessageCompressor(text_compressor=llm_lingua)
compressed_text = text_compressor.apply_transform([{"content": pdf_text}])

# print(compressed_text)

developer = ConversableAgent(
    "assistant",
    llm_config=llm_config,
    max_consecutive_auto_reply=1,
    system_message = "You are a world class SAP developer that excels in creating a TSD.",
    human_input_mode="NEVER",
)

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

developer.register_for_llm(name="testing", description="For verification of the Techincal Specification Document (TSD). It returns a list of parmeters/filters which generated TSD lacked.")(testing)
user_proxy.register_for_execution(name="testing")(testing)

context_handling = transform_messages.TransformMessages(transforms=[text_compressor])
context_handling.add_to_agent(developer)

print("///////////////////////////////////////////////////////////////////////////////////////////////")
print(compressed_text)
print("///////////////////////////////////////////////////////////////////////////////////////////////")

message = "Verify this text using the testing function : " + str(compressed_text)
result = user_proxy.initiate_chat(recipient=developer, clear_history=True, message=message, silent=True)

