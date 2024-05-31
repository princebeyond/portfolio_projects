#!/usr/bin/python3

from transformers import GPT2Tokenizer, GPT2Model

# Define the path to the model cache directory
model_path = "/home/ubuntu/.cache/huggingface/hub/models--gpt2/snapshots/607a30d783dfa663caf39e06633721c8d4cfcd7e"

# Load the tokenizer and model using the paths
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2Model.from_pretrained(model_path)

# Test the model with a simple input
inputs = tokenizer("Hello, world!", return_tensors="pt")
outputs = model(**inputs)

print(outputs)

