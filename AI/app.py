from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure the GenAI client
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/About')
def landing():
    return render_template('landing.html')

def remove_code_blocks(text):
    """Removes lines that likely represent code blocks by checking delimiters."""
    lines = text.split('\n')
    cleaned_lines = []
    in_code_block = False
    for line in lines:
        if line.startswith("```") or line.startswith("~~~"):
            in_code_block = not in_code_block  # Toggle code block state
        # Allow code blocks to be included instead of removed
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '')

    try:
        # Call the GenAI API with the provided prompt
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        # Check if response contains image data
        if hasattr(response, 'images'):
            images = response.images  # Get generated images
            image_urls = [image.url for image in images]  # Assuming the images have 'url' attribute
            return jsonify({"images": image_urls})

        generated_text = response.text  # Get the generated content
        cleaned_text = remove_code_blocks(generated_text)

        app.logger.info(f"Generated response: {cleaned_text}")
        return jsonify({"response": cleaned_text})

    except Exception as e:
        error_message = f"Exception: {str(e)}"
        app.logger.error(error_message)
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

