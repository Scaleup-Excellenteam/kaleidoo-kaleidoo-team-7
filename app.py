import os
import logging
from flask import Flask, request, jsonify, render_template
from config import Config
from models import sbert_model, genai_model
from TextProcessorSingleton import TextProcessorSingleton

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Initialize the main logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', handlers=[
    logging.FileHandler("logs/app.log"),
    logging.StreamHandler()
])

# Create a new logger for token count
token_count_logger = logging.getLogger('token_count_logger')
token_count_handler = logging.FileHandler('logs/token_count.log')
token_count_handler.setLevel(logging.INFO)
token_count_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
token_count_handler.setFormatter(token_count_formatter)

# Add the token count handler to the logger
token_count_logger.addHandler(token_count_handler)

text_processor = TextProcessorSingleton.get_instance()

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
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
        logging.debug(f"Generated response: {response.text} | Best match: {best_match}")

        # Log token count separately
        input_tokens = len(prompt.split())  # Example for counting tokens
        response_tokens = len(response.text.split())  # Example for counting tokens
        total_tokens = input_tokens + response_tokens

        token_count_logger.info(f"Input Tokens: {input_tokens}, Response Tokens: {response_tokens}, Total Tokens: {total_tokens}")

        return jsonify({'message': response.text})

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logging.info("Starting Flask app")
    app.run(debug=True)
