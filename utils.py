# utils.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def find_best_match(query, data, model, embeddings, top_k=5):
    """
    Finds the top_k best matches for the query in the data using SBERT embeddings.
    
    Args:
        query (str): The search query.
        data (list): List of data strings to search within.
        model: The SBERT model.
        embeddings (np.array): Precomputed embeddings for the data.
        top_k (int): Number of top matches to return.
    
    Returns:
        list: Top_k best matching data entries.
    """
    query_embedding = model.encode([query], convert_to_numpy=True)
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]
    best_matches = [data[idx] for idx in top_indices]
    return best_matches
