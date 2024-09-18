import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from DatabaseManager import DatabaseManager  # Assuming you have the DatabaseManager class defined elsewhere

class TextProcessor:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the TextProcessor with a SentenceTransformer model.
        """
        # Initialize SBERT model for embedding
        self.sbert_model = SentenceTransformer(model_name)
        self.db_manager = DatabaseManager()  # Initialize the database manager

    def encode_text(self, text):
        """
        Encode a single text using SBERT to create an embedding.

        Parameters:
        - text: The text to encode.

        Returns:
        - Embedding as a numpy array.
        """
        embedding = self.sbert_model.encode([text], convert_to_numpy=True)[0]
        return embedding

    def encode_and_store_data(self, texts):
        """
        Encode texts using SBERT and store them in the SQLite database.

        Parameters:
        - texts: List of texts to encode and store.
        """
        # Encode texts
        embeddings = self.sbert_model.encode(texts, convert_to_numpy=True)

        # Store texts and embeddings in the database
        for text, embedding in zip(texts, embeddings):
            self.db_manager.insert_text_and_embedding(text, embedding)

    def add_text(self, text):
        """
        Add a single text to the database by encoding it and storing it.

        Parameters:
        - text: The text to add to the database.
        """
        # Encode the text
        embedding = self.encode_text(text)

        # Store the text and embedding in the database
        self.db_manager.insert_text_and_embedding(text, embedding)

    def find_best_match(self, query, top_k=1):
        """
        Find the best matching text(s) for the given query based on cosine similarity using Faiss.

        Parameters:
        - query: The query text to find matches for.
        - top_k: Number of top matches to return.

        Returns:
        - List of tuples containing (text, similarity_score).
        """
        # Load current embeddings from the database
        texts, sbert_embeddings = self.db_manager.get_all_embeddings()

        # Normalize embeddings for cosine similarity
        sbert_embeddings = sbert_embeddings / np.linalg.norm(sbert_embeddings, axis=1, keepdims=True)

        # Initialize Faiss index with inner product (equivalent to cosine similarity after normalization)
        embedding_dim = sbert_embeddings.shape[1]
        index = faiss.IndexFlatIP(embedding_dim)  # Inner Product index
        index.add(sbert_embeddings)  # Add embeddings to the index

        # Compute the embedding for the query
        query_embedding = self.encode_text(query)
        query_embedding = query_embedding / np.linalg.norm(query_embedding)  # Normalize query embedding

        # Reshape query_embedding to 2D
        query_embedding = query_embedding.reshape(1, -1)

        # Perform search using Faiss
        distances, indices = index.search(query_embedding, top_k)

        # Retrieve best matches
        best_matches = [(texts[idx], distances[0][i]) for i, idx in enumerate(indices[0])]

        return best_matches

    def close(self):
        """
        Close the database connection.
        """
        self.db_manager.close()