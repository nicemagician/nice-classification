# backend/app.py

from fastapi import FastAPI, Request
from openai import OpenAI
from pinecone import Pinecone
import os

app = FastAPI()

# Load API keys
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pinecone.Index(os.getenv("PINECONE_INDEX", "nice-classification"))

@app.post("/classify")
async def classify(request: Request):
    data = await request.json()
    query = data.get("query")

    # Step 1: Embed the query
    vec = openai.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    ).data[0].embedding

    # Step 2: Query Pinecone for similar terms
    results = index.query(
        vector=vec,
        top_k=5,
        include_metadata=True
    ).matches

    context = "\n".join([m.metadata["text"] for m in results])

    # Step 3: Ask GPT-4o using context
    messages = [
        {"role": "system", "content": "You are a NICE classification expert. Answer in English, French or Spanish based on the user's question."},
        {"role": "user", "content": f"Using this context:\n{context}\n\nQuestion: {query}"}
    ]

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    return {"answer": response.choices[0].message.content}
