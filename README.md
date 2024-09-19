
# Tel Hai Study Buddy - Chatbot MVP

## Project Overview

Tel Hai Study Buddy is a multimodal chatbot designed to assist students at Tel Hai College in accessing lecture materials across various formats (documents, videos, and audio). The project demonstrates the feasibility of such a tool by implementing a Minimum Viable Product (MVP) with core features.

## Core Features

- **Multimodal Search**: 
  Search across documents, videos, and audio files to retrieve relevant lecture materials.
  
- **Natural Language Queries**: 
  Support for natural language input to search for specific topics or materials.

- **Timestamped Results**: 
  Provides direct access to relevant portions of video and audio materials.

## Setup Instructions

### Requirements

- Python 3.8+
- Required libraries (detailed in `requirements.txt`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/tel-hai-study-buddy.git
   cd tel-hai-study-buddy
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## Folder Structure

- `app.py`: The main Flask application to run the chatbot.
- `models.py`: Model initialization for text processing and AI-based response generation.
- `AudioTranscription.py`: Module for audio transcription using Whisper.
- `VideoTranscription.py`: Video processing and object detection using YOLO.
- `data_loader.py`: Handles loading of media files for processing.
- `DatabaseManager.py`: Manages the SQLite database for storing and retrieving embeddings.
- `TextProcessor.py`: Centralized text processing and search capabilities.
- `index.html`: Basic interface for interacting with the chatbot.

## Future Enhancements

- Personalized recommendations.
- Multi-user support and advanced filtering.

## Contributors

- Rami Hana
- Lior Silberman
- Omer Levi
- Matan Yakir
- Ehsan Ganim
