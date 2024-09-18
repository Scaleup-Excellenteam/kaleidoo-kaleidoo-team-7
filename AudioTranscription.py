import torch
from faster_whisper import WhisperModel
from sentence_transformers import SentenceTransformer
from DatabaseManager import DatabaseManager

# Initialize device and model parameters
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

model_size = "small"
compute_type = "int8" if device == "cpu" else "float16"

# Load the Whisper model
whisper_model = WhisperModel(model_size, device=device, compute_type=compute_type)

# Initialize SBERT model for embedding
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')


# Transcribe audio file
def transcribe_and_save(audio_file):
    # Transcribe audio using Whisper
    segments, info = whisper_model.transcribe(audio_file, beam_size=1)
    transcription = ''.join(segment.text for segment in segments)

    # Encode the transcription to create an embedding
    embedding = sbert_model.encode([transcription], convert_to_numpy=True)[0]

    # Save the transcription and embedding to the database
    db_manager = DatabaseManager()
    db_manager.insert_text_and_embedding(transcription, embedding)
    db_manager.close()

    print(f"Transcription for '{audio_file}' added to the database!")