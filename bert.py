import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import time
import numpy as np
import torch


# sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

# with open('database.json', 'r', encoding='utf-8') as file:
#     json_data = json.load(file)

# data = [item['data'] for item in json_data]


# sbert_embeddings = sbert_model.encode(data, convert_to_numpy=True)

def find_best_match(query, texts, sbert_model, sbert_embeddings, top_k=2):
    """
    Finds the best matching text(s) for the given query based on cosine similarity.

    Parameters:
    - query (str): The user query string.
    - texts (List[str]): List of texts to compare against.
    - sbert_model (SentenceTransformer): The Sentence Transformers model.
    - sbert_embeddings (np.ndarray): Precomputed embeddings of the texts.
    - top_k (int): Number of top matches to return.

    Returns:
    - List of tuples containing (text, similarity_score)
    """
    query_embedding = sbert_model.encode([query], convert_to_numpy=True)

    similarities = cosine_similarity(query_embedding, sbert_embeddings)[0]

    top_indices = similarities.argsort()[-top_k:][::-1]

    best_matches = [(texts[idx], similarities[idx]) for idx in top_indices]

    return best_matches

# Find the best match

