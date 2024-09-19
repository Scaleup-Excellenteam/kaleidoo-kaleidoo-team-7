import unittest

import unittest
import torch
from faster_whisper import WhisperModel
from sentence_transformers import SentenceTransformer


class TestTranscriptionIntegration(unittest.TestCase):

    def setUp(self):
        # Set up Whisper model and SentenceTransformer
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model_size = "small"
        compute_type = "int8" if device == "cpu" else "float16"

        # Initialize the actual Whisper model
        self.whisper_model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def test_transcribe_audio(self):
        # Path to the audio file to be tested
        audio_file = 'test1.mp3'  # Replace with an actual file path

        # Transcribe the audio using the actual Whisper model
        segments, info = self.whisper_model.transcribe(audio_file, beam_size=1)
        transcription = ''.join(segment.text for segment in segments)

        # Check if transcription is non-empty and is a string
        self.assertTrue(isinstance(transcription, str), "Transcription is not a string.")
        self.assertTrue(len(transcription) > 0, "Transcription is empty.")

        # Expected transcription output
        expected_transcription = "Hello everyone, how are you today? Nice to meet you. Bye bye."
        self.assertEqual(transcription.strip(), expected_transcription,
                         "Transcription does not match the expected output.")

        # Print out the transcription for review
        print(f"Transcription for '{audio_file}': {transcription}")