from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

app = Flask(__name__)

# Load the GPT-2 model and tokenizer
model_name = "gpt2-medium"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Ensure pad token is set to eos token
if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '')
    max_length = data.get('max_length', 100)
    num_return_sequences = data.get('num_return_sequences', 1)
    do_sample = data.get('do_sample', True)
    temperature = data.get('temperature', 1.0)
    top_k = data.get('top_k', 50)
    top_p = data.get('top_p', 0.95)

    # Print received data for debugging
    print(f"Received data: {data}")

    # Encode the prompt
    input_ids = tokenizer.encode(prompt, return_tensors='pt')

    # Generate responses
    outputs = model.generate(
        input_ids=input_ids,
        max_length=max_length,
        num_return_sequences=num_return_sequences,
        do_sample=do_sample,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        pad_token_id=tokenizer.eos_token_id  # Ensure pad token is set
    )

    # Decode the generated responses
    responses = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

    # Print generated responses for debugging
    print(f"Generated responses: {responses}")

    return jsonify(responses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

