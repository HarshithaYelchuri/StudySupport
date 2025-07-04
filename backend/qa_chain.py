import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def ask_question(context, question):
    prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{question}

Only answer based on the context.
"""

    response = model.generate_content(prompt)
    return response.candidates[0].content.parts[0].text.strip()
