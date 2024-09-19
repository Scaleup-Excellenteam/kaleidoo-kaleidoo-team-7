import os
from DocumentsParser import extract_text_from_file


DOCS_DIRECTORY = './docs'

# List all files in the directory
uploaded = [os.path.join(DOCS_DIRECTORY, filename) for filename in os.listdir(DOCS_DIRECTORY) if filename.endswith(('.docx', '.pdf', '.txt', '.pptx'))]

# Process all uploaded files
for idx, filename in enumerate(uploaded):
    print(f"Processing File {idx + 1}/{len(uploaded)}: {filename}")
    try:
        text, file_type = extract_text_from_file(filename)
        if not text:
            print(f"Error processing {filename}: No text found")
        else:
            print(f"Successfully processed {filename}: {len(text)} characters extracted")

    except Exception as e:
        print(f"Error processing {filename}: {e}")