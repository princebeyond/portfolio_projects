#!/usr/bin/python3

from flask import Flask, request, jsonify
import anthropic

# Remove hardcoded API key (replace with steps to use environment variables)
API_KEY = ""

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '')

    try:
        # Use environment variable for API key
        client = Anthropic(api_key=os.environ.get('API_KEY'))  # Replace with your environment variable name

        # Call the Claude API with the prompt
        generated_text = client.call(prompt)
        app.logger.info(f"Generated response: {generated_text}")
        return jsonify({"response": generated_text})

    except anthropic.errors.AnthropicError as e:
        error_message = f"Anthropic Error: {str(e)}"
        app.logger.error(error_message)
        return jsonify({"error": error_message}), 500

    except Exception as e:
        error_message = f"Exception: {str(e)}"
        app.logger.error(error_message)
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

