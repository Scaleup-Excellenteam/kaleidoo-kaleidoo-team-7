# models.py
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from config import Config

# Initialize SBERT model
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

# Configure Generative AI with API key
genai.configure(api_key=Config.API_KEY)
genai_model = genai.GenerativeModel("gemini-1.5-flash")
