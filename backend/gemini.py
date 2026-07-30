import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(question, context):
    prompt = f"""
You are an AI Document Assistant.

Answer ONLY using the context below.

If the answer is not present in the context, reply:
"I couldn't find this information in the uploaded document."

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text