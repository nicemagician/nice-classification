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
    # pinecone.create_index(name=pinecone_index, dimension=1536, metric="cosine", spec=ServerlessSpec(cloud="aws", region="us-east-1"))
index = pinecone.Index(pinecone_index)

def embed(texts):
    return openai.embeddings.create(input=texts, model="text-embedding-3-small").data

def process_csv(filepath, source):
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(tqdm(reader)):
            if source == "alphabetical":
                term = row.get("Indication", "").strip()
                text = f"Class {row.get('Class', '').strip()} – {term}"
            elif source == "ipos":
                term = row.get("Goods and Services Description", "").strip()
                text = f"Class {row.get('Class No.', '').strip()} – {term}"
            elif source == "uspto":
                term = row.get("Description", "").strip()
                text = f"Class {row.get('Class', '').strip()} – {term}"
            else:
                continue  # skip unknown format

            if not term or not text:
                continue

            vec = embed([text])[0].embedding
            index.upsert([(f"{source}-{i}", vec, {"term": term, "text": text, "source": source})])

# Process each source
process_csv("data/alphabetical_list.csv", "alphabetical")
process_csv("data/ipos_database.csv", "ipos")
process_csv("data/uspto_database.csv", "uspto")

print("✅ All data embedded and uploaded to Pinecone.")
