from ibm_docx_parser import extract_text


def split_document(text):
    # Find the start and end of the Technical Details section
    tech_details_start = text.find("**Technical Details**")
    tech_details_end = text.find("**", tech_details_start + 20)  # Look for the next section after Technical Details

    if tech_details_start == -1 or tech_details_end == -1:
        print("Could not find the Technical Details section.")
        return None, None, None

    # Split the document
    part1 = text[:tech_details_start].strip()
    part2 = text[tech_details_start:tech_details_end].strip()
    part3 = text[tech_details_end:].strip()

    return part1, part2, part3



document = data = extract_text("/Users/mahir/Desktop/Agents/Application/TSD.docx")


# Split the document
part1, part2, part3 = split_document(document)

# Write the parts to separate files
if part1 and part2 and part3:
    with open('part1.txt', 'w') as file:
        file.write(part1)
    with open('part2.txt', 'w') as file:
        file.write(part2)
    with open('part3.txt', 'w') as file:
        file.write(part3)
    print("Document successfully split into three parts.")
else:
    print("Failed to split the document.")