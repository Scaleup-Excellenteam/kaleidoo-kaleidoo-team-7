# data_loader.py
import json
from models import sbert_model

# Load data from JSON file
with open('data.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

data = []
for item in json_data:
    title = item['title']
    page = item['data']['page']
    content = item['data']['content']
    
    # Combine title, page, and content into a single string
    formatted_text = f"Title: {title} | Page: {str(page)} | Content: {content}"
    data.append(formatted_text)

# Compute SBERT embeddings
sbert_embeddings = sbert_model.encode(data, convert_to_numpy=True)
