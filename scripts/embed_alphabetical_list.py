import csv
import os
from openai import OpenAI
from tqdm import tqdm
from pinecone import Pinecone, ServerlessSpec

openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index = os.getenv("PINECONE_INDEX", "nice-classification")

openai = OpenAI(api_key=openai_api_key)
pinecone = Pinecone(api_key=pinecone_api_key)

if pinecone_index not in pinecone.list_indexes():
    pass  # index already exists

index = pinecone.Index(pinecone_index)

def embed(texts):
    return openai.embeddings.create(input=texts, model="text-embedding-3-small").data

def process_alphabetical(filepath):
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(tqdm(reader)):
            term = row.get("term", "").strip()
            description = row.get("description", "").strip()
            class_number = row.get("class_number", "").strip()
            language = row.get("language", "en").strip()
            basic_number = row.get("basic_number", "").strip()

            if not term or not class_number:
                continue

            text = f"Class {class_number} – {term}. {description}"
            metadata = {
                "term": term,
                "description": description,
                "class_number": class_number,
                "language": language,
                "basic_number": basic_number,
                "source": "alphabetical"
            }

            vec = embed([text])[0].embedding
            index.upsert([(f"alphabetical-{i}", vec, metadata)], namespace="alphabetical")

# Example usage
process_alphabetical("data/alphabetical_list.csv")

print("✅ Alphabetical List embedded and uploaded to Pinecone.")
