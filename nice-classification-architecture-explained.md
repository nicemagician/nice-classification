# 🧱 Architecture Explained – Nice Classification Assistant

This project is a small-scale RAG (Retrieval-Augmented Generation) system.

### 🔧 Technologies
- **Frontend**: React (Vite + TailwindCSS), deployed to Vercel
- **Backend**: FastAPI app deployed on Replit Reserved VM
- **Vector Search**: Pinecone for nearest-neighbor search
- **Language Model**: OpenAI (GPT-4o + Embeddings)

### 🔗 Flow
1. User enters a query on the frontend (e.g., "electric mosquito diffuser")
2. Frontend POSTs the query to `/classify` endpoint (with token)
3. Backend:
   - Embeds the query using `text-embedding-3-small`
   - Queries Pinecone for similar WIPO terms
   - Passes results + query into GPT-4o to reason and reply
4. Result is returned and displayed to user in the interface

This architecture is modular, multilingual, and WIPO-compliant.