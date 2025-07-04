import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_mcq_quiz(context, difficulty="basic", num_questions=5):
    prompt = f"""
You are a quiz master. Generate a {difficulty}-level MCQ quiz based on the following content.

Context:
{context}

Create {num_questions} multiple-choice questions. Each question should have 4 options (A, B, C, D), indicate the correct answer, and include a one-line explanation.

Format:
Q1. Question?
A. Option A
B. Option B
C. Option C
D. Option D
Answer: B
Explanation: One-line reason why B is correct
"""
    response = model.generate_content(prompt)
    return response.text.strip()

def parse_mcq_output(quiz_text):
    questions = []
    blocks = quiz_text.strip().split("Q")
    for block in blocks:
        if not block.strip():
            continue
        lines = block.strip().splitlines()
        q_line = lines[0].strip()
        options = {line[0]: line[3:].strip() for line in lines[1:5]}
        answer = re.search(r"Answer:\s*([A-D])", "\n".join(lines)).group(1)
        explanation = re.search(r"Explanation:\s*(.*)", "\n".join(lines)).group(1)
        questions.append({
            "question": q_line[q_line.find('.')+1:].strip(),
            "options": options,
            "answer": answer,
            "explanation": explanation
        })
    return questions
