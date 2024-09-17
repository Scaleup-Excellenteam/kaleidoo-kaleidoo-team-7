import torch
import json
from faster_whisper import WhisperModel
import os

# Initialize the device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Model size and compute type based on device
model_size = "small"
compute_type = "int8" if device == "cpu" else "float16"

# Load the Whisper model
model = WhisperModel(model_size, device=device, compute_type=compute_type)

# Transcribe a new audio file
def transcribe_audio(audio_file):
    segments, info = model.transcribe(audio_file, beam_size=1)

    transcription = ""
    for segment in segments:
        transcription += segment.text

    return transcription

# Path to the existing JSON file
json_file_path = 'data.json'

# Check if the JSON file exists and has content
if os.path.exists(json_file_path) and os.path.getsize(json_file_path) > 0:
    # Load existing data from the JSON file
    with open(json_file_path, 'r') as json_file:
        try:
            json_data = json.load(json_file)
        except json.JSONDecodeError:
            # If the JSON file is corrupted, initialize it as an empty structure
            json_data = {"data": []}
else:
    # If the file doesn't exist or is empty, create a new structure
    json_data = {"data": []}

# Transcribe an audio file and append the transcription
audio_file = 'test1.mp3'
transcription = transcribe_audio(audio_file)

# Append the new transcription to the 'data' key
json_data['data'].append(f"""{transcription}""")

# Write the updated data back to the JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

# Print success message
print(f"Transcription added to {json_file_path}!")
