import csv
import os
from pathlib import Path
from openai import OpenAI
from tqdm import tqdm
from pinecone import Pinecone, ServerlessSpec

# Load API keys from environment
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index = os.getenv("PINECONE_INDEX", "nice-classification")

# Initialize clients
openai = OpenAI(api_key=openai_api_key)
pinecone = Pinecone(api_key=pinecone_api_key)

# Ensure index exists
if pinecone_index not in pinecone.list_indexes():
    pass  # Assume it exists

index = pinecone.Index(pinecone_index)

def embed(texts):
    return openai.embeddings.create(input=texts, model="text-embedding-3-small").data

def process_mgs(filepath):
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(tqdm(reader, desc=f"Embedding {filepath.name}")):
            term = row.get("term", "").strip()
            description = row.get("description", "").strip()
            class_number = row.get("class_number", "").strip()
            language = row.get("language", "en").strip()

            if not term or not class_number:
                continue

            text = f"Class {class_number} – {term}. {description}"
            metadata = {
                "term": term,
                "description": description,
                "class_number": class_number,
                "language": language,
                "source": "mgs_notes"
            }

            vec = embed([text])[0].embedding
            index.upsert([(f"{filepath.stem}-{i}", vec, metadata)], namespace="mgs_notes")

# Process all MGS note files
folder = Path("data/mgs_notes/")
csv_files = sorted(folder.glob("mgs_note_class_*.csv"))

for filepath in csv_files:
    print(f"📄 Processing {filepath.name}")
    process_mgs(filepath)

print("✅ All MGS notes embedded and uploaded to Pinecone.")