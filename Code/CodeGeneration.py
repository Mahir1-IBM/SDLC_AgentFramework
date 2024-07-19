import time
import requests
from typing_extensions import Annotated

async def CodeGenAPI(
        WRICEF_type: Annotated[str, "The wricef type of the TSD."],
        input_file_path: Annotated[str, "The path for the TSD."]
    ) -> str:
    

    ####################################### SECTION MAPPING URL ###################################################
    
    url_section_mapping = f"http://127.0.0.1:8000/section-mapping?wricef_type={WRICEF_type}"

    headers_section_mapping = {
        'accept': 'application/json'
    }

    response_section_mapping = requests.post(url_section_mapping, headers=headers_section_mapping, data='')

    if response_section_mapping.status_code == 200:
        section_mapping = response_section_mapping.text
        print("Section mapping retrieved successfully : ", section_mapping)
    else:
        print(f"Failed to retrieve section mapping. Status code: {response_section_mapping.status_code}")
        print("Response:", response_section_mapping.text)
        return "1"
    



    ####################################### GENERATING MODULES URL ###################################################

    url_generating_module = f"http://127.0.0.1:8000/generate_modules/?wricef_type={WRICEF_type}&section_mapping={section_mapping}"

    headers_upload_file = {
        'accept': 'application/json'
    }

    with open(input_file_path, 'rb') as input_file:
        files = {
            'technical_specification_document': ('O2C_E_826_827_Product Allocation UK_TDS.docx', input_file, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
        }

        response_upload_file = requests.post(url_generating_module, headers=headers_upload_file, files=files)

        if response_upload_file.status_code == 200:
            response_data = response_upload_file.json() 
            status_id1 = response_data
            print("File uploaded successfully and the response is ", response_data)
        
        else:
            print(f"File upload failed. Status code: {response_upload_file.status_code}")
            print("Response:", response_upload_file.text)
            return "2"




    ####################################### GET STATUS URL ###################################################

    url_status_module = f"http://127.0.0.1:8000/get_status_module/?session_id_1={status_id1}"

    processing = True

    while processing:
        response_status = requests.post(url_status_module, headers={'accept': 'application/json'}, data='')
        
        if response_status.status_code == 200:
            status_data = response_status.json()
            if status_data['message'] == 'Completed':
                print("Processing completed. Generating code_modules ...")
                code_modules = status_data['response']['code_modules']
                file_name = status_data['response']['file_name']
                # pretty_code_modules = json.dumps(code_modules, indent=4)
                # print("code_modules " , pretty_code_modules)

                processing = False
            
            else:
                print("Processing not yet completed. Waiting for 30 seconds before checking again...")
                time.sleep(30)

        else:
            print(f"Failed to check status. Status code: {response_status.status_code}")
            print("Response:", response_status.text)
            return "3"




    ####################################### MERGE CODE URL ###################################################

    url_merge = f"http://127.0.0.1:8000/merge/?wricef_type={WRICEF_type}&filename={file_name}&session_id_1={status_id1}"


    response_merge = requests.post(url_merge, headers={'accept': 'application/json', 'Content-Type': 'application/json'}, json=code_modules)

    if response_merge.status_code == 200:
        section_mapping = response_merge.json() 
        status_id2 = section_mapping
        print("Second Status id after merging retrieved successfully : ", status_id2)
    else:
        print(f"Failed to retrieve second Status id. Status code: {response_merge.status_code}")
        print("Response:", response_merge.text)
        return "4"
    



    ####################################### GET STATUS MERGE URL ###################################################

    url_status_module = f"http://127.0.0.1:8000/get_status_merge/?session_id_2={status_id2}"

    while True:
        response_status = requests.post(url_status_module, headers={'accept': 'application/json'}, data='')
        
        if response_status.status_code == 200:
            status_data = response_status.json()
            if status_data['status'] == 'Completed':
                print("Processing completed. Generating code...")
                code = status_data['response']['merged_code']
                
                return code
            
            else:
                print("Processing not yet completed. Waiting for 30 seconds before checking again...")
                time.sleep(30)

        else:
            print(f"Failed to generate code. Status code: {response_status.status_code}")
            print("Response:", response_status.text)
            break

    return "5"



# code = CodeGenAPI("Enhancement", "/Users/mahir/Desktop/Agents/Application/CodeGen/O2C_E_826_827_Product Allocation UK_TDS.docx")
# print(code)