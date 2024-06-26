import requests

def get_section_mapping_and_upload_file() -> int:
    #Get section mapping
    # url_section_mapping = 'https://tech-spec-generation-tech-spec-gen-dev.tech-spec-gen-dev-7825badf9e223e8d936f579788da7514-0000.us-south.containers.appdomain.cloud/section-mapping?WRICEF_type=report'

    url_section_mapping = 'http://127.0.0.1:8000/section-mapping?WRICEF_type=report'
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

    # url_upload_file = 'https://tech-spec-generation-tech-spec-gen-dev.tech-spec-gen-dev-7825badf9e223e8d936f579788da7514-0000.us-south.containers.appdomain.cloud/uploadfile/'
    # data = {
    #     'user_id': 'Mahir.Jain1@ibm.com',
    #     'tsd_type': 'Initial',
    #     'WRICEF_type': 'report',
    # }

    # url_upload_file = 'https://tech-spec-generation-tech-spec-gen-dev.tech-spec-gen-dev-7825badf9e223e8d936f579788da7514-0000.us-south.containers.appdomain.cloud/uploadfile/?user_id=Mahir.Jain1@ibm.com&tsd_type=Initial&WRICEF_type=report'

    url_upload_file = 'http://127.0.0.1:8000/uploadfile/?user_id=Mahir.Jain1%40ibm.com&tsd_type=Initial&WRICEF_type=report'

    # user_id=Mahir.Jain1%40ibm.com&tsd_type=Initial&WRICEF_type=repor
    headers_upload_file = {
        'accept': 'application/json'
    }

    input_file_path = '/Users/mahir/Desktop/Agents/Application/FS RDD0304 - QM _Batch Genealogy Report V1.0 report.docx'

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

if __name__ == "__main__":
    get_section_mapping_and_upload_file()
