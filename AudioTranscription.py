import torch
from faster_whisper import WhisperModel
from sentence_transformers import SentenceTransformer
from TextProcessorSingleton import TextProcessorSingleton

text_processor = TextProcessorSingleton.get_instance()

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

    # Use the TextProcessor's add_text function to add the transcription and its embedding
    text_processor.add_text(transcription)

    # Close the database connection
    text_processor.close()

    print(f"Transcription for '{audio_file}' added to the database!")