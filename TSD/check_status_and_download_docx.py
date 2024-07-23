import time
import requests
from typing_extensions import Annotated


def check_status_and_download_docx(
        user_id: Annotated[str, "The user id of the user."],
        output_path: Annotated[str, "The path where the generated TSD is saved locally."]
    ) -> int:
    
    # status_url = f'https://tech-spec-generation-tech-spec-gen-dev.tech-spec-gen-dev-7825badf9e223e8d936f579788da7514-0000.us-south.containers.appdomain.cloud/get-status?user_id={user_id}'
    status_url = f"http://127.0.0.1:8001/get-status?user_id={user_id}"
    while True:
        response_status = requests.post(status_url, headers={'accept': 'application/json'}, data='')
        
        if response_status.status_code == 200:
            status_data = response_status.json()
            entry = status_data[0]
            print(entry['timestamp'])
            if entry['status'] == 'Completed':
                print("Processing completed. Downloading document...")
                dox_link = entry['docx_link']
                
                # Download the document

                docx_response = requests.get(dox_link)
                if docx_response.status_code == 200:
                    return dox_link
                    # with open(output_path, 'wb') as file:
                    #     file.write(docx_response.content)
                    # print(f"Document downloaded successfully and saved to {output_path}")
                else:
                    print(f"Failed to download the document. Status code: {docx_response.status_code}")
                
                return 0
            
            else:
                print("Processing not yet completed. Waiting for 60 seconds before checking again...")
                time.sleep(60)

        else:
            print(f"Failed to check status. Status code: {response_status.status_code}")
            print("Response:", response_status.text)
            break
    
    return 0

