import os
from DocumentsParser import extract_text_from_file
from AudioTranscription import transcribe_and_save
from VideoTranscription import process_video_detection
DOCS_DIRECTORY = './docs'

# List all files in the directory
uploaded = [os.path.join(DOCS_DIRECTORY, filename) for filename in os.listdir(DOCS_DIRECTORY) if filename.endswith(('.docx', '.pdf', '.pptx'))]
audio_files = [os.path.join(DOCS_DIRECTORY, filename) for filename in os.listdir(DOCS_DIRECTORY) 
               if filename.endswith(('.mp3'))]
video_files = [os.path.join(DOCS_DIRECTORY, filename) for filename in os.listdir(DOCS_DIRECTORY) 
               if filename.endswith(('.mp4'))]
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

for idx, filename in enumerate(audio_files):
    print(f"Processing Audio File {idx + 1}/{len(audio_files)}: {filename}")
    try:
        transcribe_and_save(filename)
        print(f"Successfully transcribed {filename}")
    except Exception as e:
        print(f"Error processing {filename}: {e}")
# for idx, filename in enumerate(video_files):
#     print(f"Processing Video File {idx + 1}/{len(video_files)}: {filename}")
#     try:
#         transcribe_and_save(filename)
#         print(f"Successfully transcribed {filename}")
#     except Exception as e:
#         print(f"Error processing {filename}: {e}")