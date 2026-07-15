import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_embedding(text):
       result = genai.embed_content(
           model="models/gemini-embedding-001",
           content=text,
           output_dimensionality=768
       )
       return result["embedding"] 