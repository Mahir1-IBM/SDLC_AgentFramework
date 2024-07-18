import os
import autogen

import requests
from bs4 import BeautifulSoup
import json
from typing import Annotated
from autogen.coding import LocalCommandLineCodeExecutor
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain import PromptTemplate
from langchain_openai import AzureChatOpenAI
from autogen import ConversableAgent, config_list_from_json, AssistantAgent


config_list = config_list_from_json(
    env_or_file = "OAI_CONFIG_LIST.json"
)

llm_config = {
    "config_list" : config_list, 
    "timeout" : 120
}


os.environ["AZURE_OPENAI_API_KEY"] = "ba3bfb17a7b5470295ec96431d4b07c0"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://openai-dtt-cic-sj.openai.azure.com"
os.environ["AZURE_OPENAI_API_VERSION"] = "2024-02-15-preview"
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "gpt4-32k"

temp_dir = "/Users/mahir/Desktop/Agents/Application/codingProject"


model = AzureChatOpenAI(
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
)

executor = LocalCommandLineCodeExecutor(
    timeout=500,  
    work_dir=temp_dir,  
)


def scrape(url: str):
    # scrape website, and also will summarize the content based on objective if the content is too large
    # objective is the original objective & task that user give to the agent, url is the url of the website to be scraped

    print("Scraping website...")
    # Define the headers for the request
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
    }

    # Define the data to be sent in the request
    data = {
        "url": url
    }

    # Convert Python object to JSON string
    data_json = json.dumps(data)

    # Send the POST request
    response = requests.post(
        "https://chrome.browserless.io/content?token=2db344e9-a08a-4179-8f48-195a2f7ea6ee", headers=headers, data=data_json)

    # Check the response status code
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


def research(query) -> str:
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
        max_consecutive_auto_reply=2,
        human_input_mode="TERMINATE",
        function_map={
            "scrape": scrape,
        }
    )

    user_proxy.initiate_chat(researcher, message=f"here's the url to scrape : {query}")

    # set the receiver to be researcher, and get a summary of the research report
    user_proxy.stop_reply_at_receive(researcher)
    user_proxy.send(
        "Give me a list of parameter from the generated result, return ONLY the list", researcher)

    # return the last message the expert received
    result = user_proxy.last_message()["content"]
    # print("here is the parameter list: ", result)
    
    return result


async def verification_Scraping(
        data : Annotated[str, "TSD data that needs to be verified."],
        params:  Annotated[str, "List of parameters that TSD does not verify"],
    ) -> str:
    
    url = 'https://community.sap.com/t5/forums/searchpage/tab/message?q=TSD&collapse_discussion=true'
    result = research(url)

    Validator = AssistantAgent(
        name="Agent_to_verify_TSD",
        system_message=f"You are a very skilled AI agent. Check the {data} and then thusing the list : {result} make sure that the list of parameters that TSD did not verify : {params} are indeed correct or not. When the verification is done return 'TERMINATE'.",
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
        Validator, message="Read the generated TSD and then verify the list of parameters it did not verify using your knowldge. Return the parameters which were not satisfied by the TSD.")
    
    user_proxy.stop_reply_at_receive(Validator)
    user_proxy.send(
        "Give me a list of parameter that the generated result did not verify, with a proper explaination of each point.", Validator)

    # return the last message the expert received
    return user_proxy.last_message()["content"]
    


# url = 'https://community.sap.com/t5/forums/searchpage/tab/message?q=TSD&collapse_discussion=true'
# result = research(url)
# print("here is the parameter list: ", result)