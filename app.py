from flask import Flask, request, jsonify, render_template
from bert import find_best_match
from sentence_transformers import SentenceTransformer
import json


sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

with open('data.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

data = [item['data'] for item in json_data]


sbert_embeddings = sbert_model.encode(data, convert_to_numpy=True)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    search_text = request.form.get('search')  # Get the text from the form
    best_matches = find_best_match(search_text, data, sbert_model, sbert_embeddings, top_k=5)
    # return jsonify(best_matches)  # Return JSON response
    return jsonify({'message': f'You searched for: {best_matches[0][0]}'})  # Return JSON response


if __name__ == '__main__':
    app.run(debug=True)