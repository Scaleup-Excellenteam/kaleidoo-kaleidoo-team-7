import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer


class DatabaseManager:
    def __init__(self, db_path='application_data.db'):
        """
        Initialize the database manager and connect to the SQLite database.
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()


    def create_tables(self):
        """
        Create necessary tables if they do not exist.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS texts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS embeddings (
                id INTEGER PRIMARY KEY,
                embedding BLOB,
                FOREIGN KEY (id) REFERENCES texts(id)
            )
        ''')
        self.conn.commit()

    def insert_text_and_embedding(self, text, embedding):
        """
        Insert a new text and its corresponding embedding into the database.
        """
        try:
            # Insert text
            self.cursor.execute('INSERT INTO texts (text) VALUES (?)', (text,))
            text_id = self.cursor.lastrowid

            # Insert embedding
            self.cursor.execute('INSERT INTO embeddings (id, embedding) VALUES (?, ?)',
                                (text_id, embedding.tobytes()))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Text '{text[:30]}...' already exists in the database.")

    def delete_detection(self, text, embedding):
        """
        Insert a new text and its corresponding embedding into the database.
        """
        try:
            # Insert text
            self.cursor.execute('INSERT INTO texts (text) VALUES (?)', (text,))
            text_id = self.cursor.lastrowid

            # Insert embedding
            self.cursor.execute('INSERT INTO embeddings (id, embedding) VALUES (?, ?)',
                                (text_id, embedding.tobytes()))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Text '{text[:30]}...' already exists in the database.")

    def get_all_embeddings(self):
        """
        Retrieve all texts and embeddings from the database.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT text, embedding FROM texts JOIN embeddings ON texts.id = embeddings.id')
            rows = cursor.fetchall()
            texts = [row[0] for row in rows]
            embeddings = np.array([np.frombuffer(row[1], dtype=np.float32) for row in rows])
        finally:
            cursor.close()
            conn.close()
        return texts, embeddings


    def close(self):
        """
        Close the connection to the SQLite database.
        """
        self.conn.close()

    def clear_table(self, table_name):
        """
        Clear all data from the specified table.
        """
        try:
            self.cursor.execute(f'DELETE FROM {table_name}')
            self.conn.commit()
            print(f"All data from the table '{table_name}' has been cleared.")
        except sqlite3.Error as e:
            print(f"An error occurred while clearing the table '{table_name}': {e}")

    def clear_all_tables(self):
        """
        Clear all data from all tables in the database.
        """
        try:
            self.clear_table('embeddings')
            self.clear_table('texts')
            print("All tables have been cleared.")
        except sqlite3.Error as e:
            print(f"An error occurred while clearing all tables: {e}")
    def display_table(self, table_name):
        """
        Display all rows from the specified table.
        """
        try:
            self.cursor.execute(f'SELECT * FROM {table_name}')
            rows = self.cursor.fetchall()
            for row in rows:
                print(row)
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
