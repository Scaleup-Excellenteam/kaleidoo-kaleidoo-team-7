# app.py
from flask import Flask, request, jsonify, render_template
from config import Config
from models import sbert_model, genai_model
from data_loader import data, sbert_embeddings
from utils import find_best_match

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        search_text = request.form.get('search')
        if not search_text:
            return jsonify({'error': 'No search query provided.'}), 400

        best_match = find_best_match(search_text, data, sbert_model, sbert_embeddings, top_k=5)
        


        prompt = f"""
        Generate a comprehensive response based on the following:

        **Query:** {search_text}

        **Most Similar SBERT Answer Embedding:** {best_match}

        **Response Format:** Informative and concise.
        """

        # Generate the response using the generative AI model
        response = genai_model.generate_content(prompt)

        return jsonify({'message': f'You searched for: {response.text}'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
