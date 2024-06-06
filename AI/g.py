#!/usr/bin/python3

import google.generativeai as genai
import os
from google.generativeai import generative_models

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = generative_models.GenerativeModel.from_pretrained("gemini-1.5-flash")
response = model.generate_content("Write a story about a magic backpack.")
print(response.text)
