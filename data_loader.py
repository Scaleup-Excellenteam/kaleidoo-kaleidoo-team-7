# data_loader.py
import json
from models import sbert_model

# Load data from JSON file
with open('data.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

data = [item['data'] for item in json_data]

# Compute SBERT embeddings
sbert_embeddings = sbert_model.encode(data, convert_to_numpy=True)
