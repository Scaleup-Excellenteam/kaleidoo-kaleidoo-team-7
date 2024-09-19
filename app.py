import logging
from flask import Flask, request, jsonify, render_template
from config import Config
from models import sbert_model, genai_model
# from utils import find_best_match
from TextProcessor import text_processor

# Initialize logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', handlers=[
    logging.FileHandler("app.log"),
    logging.StreamHandler()
])

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    logging.info("Home page accessed")
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        search_text = request.form.get('search')

        if not search_text:
            logging.warning("No search query provided")
            return jsonify({'error': 'No search query provided.'}), 400

        logging.info(f"Search query received: {search_text}")
        
        # Find best match using text_processor
        best_match = text_processor.find_best_match(search_text, top_k=5)
        logging.debug(f"Best match: {best_match}")

        # Generate the prompt for the generative AI model
        prompt = f"""
        Generate a comprehensive and informative response in the same language as the provided information.

        Best Match: {best_match}

        Response Format: Informative and concise in the context of the query: {search_text}.
        At the end of the answer, write the title from which the answer was taken.

        If you can't find an answer to a query, write "Sorry, I don't have enough knowledge to answer this for you".
        """

        # Generate the response using the generative AI model
        response = genai_model.generate_content(prompt)
        logging.debug(f"Generated response: {response} | Best match: {best_match}")

        return jsonify({'message': response})

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logging.info("Starting Flask app")
    app.run(debug=True)