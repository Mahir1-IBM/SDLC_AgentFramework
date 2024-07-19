import requests

def get_section_mapping_and_upload_file(user_id: str, tsd_type: str, WRICEF_type: str, input_file_path: str) -> int:
     
    # /////////////////////////////////////// Get section mapping URL/////////////////////////////////////// 
    
    # url_section_mapping = f'https://tech-spec-generation-tech-spec-gen-dev.tech-spec-gen-dev-7825badf9e223e8d936f579788da7514-0000.us-south.containers.appdomain.cloud/section-mapping?WRICEF_type={WRICEF_type}'
    url_section_mapping = f'http://127.0.0.1:8001/section-mapping?WRICEF_type={WRICEF_type}'
    headers_section_mapping = {
        'accept': 'application/json'
    }

    response_section_mapping = requests.post(url_section_mapping, headers=headers_section_mapping, data='')

    if response_section_mapping.status_code == 200:
        section_mapping = response_section_mapping.text
        print("Section mapping retrieved successfully")
    else:
        print(f"Failed to retrieve section mapping. Status code: {response_section_mapping.status_code}")
        print("Response:", response_section_mapping.text)
        return

    
    # /////////////////////////////////////// Construct upload file URL ///////////////////////////////////////
    
    # url_upload_file = f'https://tech-spec-generation-tech-spec-gen-dev.tech-spec-gen-dev-7825badf9e223e8d936f579788da7514-0000.us-south.containers.appdomain.cloud/uploadfile/?user_id={user_id}&tsd_type={tsd_type}&WRICEF_type={WRICEF_type}'
    url_upload_file = f'http://127.0.0.1:8001/uploadfile/?user_id={user_id}&tsd_type={tsd_type}&WRICEF_type={WRICEF_type}'
    
    headers_upload_file = {
        'accept': 'application/json'
    }

    with open(input_file_path, 'rb') as input_file:
        files = {
            'input_fsd': ('FS RDD0304 - QM _Batch Genealogy Report V1.0 report.docx', input_file, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
            'section_mapping': (None, section_mapping, 'application/json')
        }

        response_upload_file = requests.post(url_upload_file, headers=headers_upload_file, files=files)

        if response_upload_file.status_code == 200:
            print("File uploaded successfully")
        else:
            print(f"File upload failed. Status code: {response_upload_file.status_code}")
            print("Response:", response_upload_file.text)

    return 0

# if __name__ == "__main__":

#     user_id = 'Mahir.Jain1@ibm.com'
#     tsd_type = 'Initial'
#     WRICEF_type = 'report'
#     input_file_path = 'FS RDD0304 - QM _Batch Genealogy Report V1.0 report.docx'
#     get_section_mapping_and_upload_file(user_id, tsd_type, WRICEF_type, input_file_path)
