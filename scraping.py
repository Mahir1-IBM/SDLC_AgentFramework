import os
import autogen
import requests
from bs4 import BeautifulSoup
import json
from autogen.coding import LocalCommandLineCodeExecutor
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain import PromptTemplate
from langchain_openai import AzureChatOpenAI
import agentops
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize AgentOps
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
if not AGENTOPS_API_KEY:
    raise ValueError("AGENTOPS_API_KEY not found in environment variables")

agentops.init(AGENTOPS_API_KEY)

os.environ["AZURE_OPENAI_API_KEY"] = "ba3bfb17a7b5470295ec96431d4b07c0"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://openai-dtt-cic-sj.openai.azure.com"
os.environ["AZURE_OPENAI_API_VERSION"] = "2024-02-15-preview"
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "gpt4-32k"

temp_dir = "/Users/mahir/Desktop/Agents/Application/codingProject"

@agentops.record_function('initialize_model_and_executor')
def initialize_model_and_executor():
    model = AzureChatOpenAI(
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    )

    executor = LocalCommandLineCodeExecutor(
        timeout=500,  
        work_dir=temp_dir,  
    )
    return model, executor

model, executor = initialize_model_and_executor()

@agentops.record_function('scrape')
def scrape(url: str):
    print("Scraping website...")
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
    }
    data = {
        "url": url
    }
    data_json = json.dumps(data)
    response = requests.post(
        "https://chrome.browserless.io/content?token=2db344e9-a08a-4179-8f48-195a2f7ea6ee", headers=headers, data=data_json)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        print("CONTENT:", text)
        if len(text) > 8000:
            output = summary(text)
            return output
        else:
            return text
    else:
        print(f"HTTP request failed with status code {response.status_code}")

@agentops.record_function('summary')
def summary(content):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)
    docs = text_splitter.create_documents([content])
    map_prompt = """
    Write a detailed summary of the following text for a generating a list of parameters to check or verify the TSD:
    "{text}"
    SUMMARY:
    """
    map_prompt_template = PromptTemplate(
        template=map_prompt, input_variables=["text"])

    summary_chain = load_summarize_chain(
        llm=model,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,
        combine_prompt=map_prompt_template,
        verbose=True
    )

    output = summary_chain.run(input_documents=docs,)
    return output

@agentops.record_function('research')
def research(query):
    llm_config_researcher = {
        "functions": [
            {
                "name": "scrape",
                "description": "Scraping website content based on url and collecting parameters for TSD",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "Website url to scrape",
                        }
                    },
                    "required": ["url"],
                },
            },
        ],
        "config_list" : [
            {
                "model" : "gpt4-32k",
                "base_url": "https://openai-dtt-cic-sj.openai.azure.com",
                "api_key": "ba3bfb17a7b5470295ec96431d4b07c0",
                "api_type": "azure",
                "api_version": "2024-02-15-preview"
            }
        ]
    }

    researcher = autogen.AssistantAgent(
        name="researcher",
        system_message="Research about the TSD documents using the url, collect as many information as possible, and get a detailed understanding with loads of technique details about the SAP pipeline and TSD documents. Prepare a list of things that a TSD must have.; Add TERMINATE to the end of the research report;",
        llm_config=llm_config_researcher,
    )

    user_proxy = autogen.UserProxyAgent(
        name="User_proxy",
        code_execution_config={"executor": executor, "last_n_messages" : 2},
        is_termination_msg=lambda x: x.get("content", "") and x.get(
            "content", "").rstrip().endswith("TERMINATE"),
        human_input_mode="TERMINATE",
        function_map={
            "scrape": scrape,
        }
    )

    user_proxy.initiate_chat(researcher, message=f"here's the url to scrape : {query}")

    user_proxy.stop_reply_at_receive(researcher)
    user_proxy.send(
        "Give me a list of parameter from the generated result, return ONLY the list", researcher)

    return user_proxy.last_message()["content"]

@agentops.record_function('main')
def main():
    url = 'https://community.sap.com/t5/forums/searchpage/tab/message?q=TSD&collapse_discussion=true'
    result = research(url)
    print("here is the parameter list: ", result)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        agentops.log_error(str(e))
    finally:
        agentops.end_session('Success')