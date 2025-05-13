# An AI-powered NICE classification assistant.

## 🔧 Setup Instructions
1. Clone the repo
2. Put your classification data into `data/`
3. Set API keys in `.env`
4. Run `scripts/embed_data.py` to index your data
5. Start the API with `uvicorn backend.app:app --reload`

## 🌍 Deployment
- Use Vercel for frontend
- Use Replit or Railway for backend
- Use Pinecone free tier for vector DB

## 📦 .env.example
```env
OPENAI_API_KEY=your_openai_key_here
PINECONE_API_KEY=your_pinecone_key_here
PINECONE_INDEX=nice-classification
```

---

## 🗺️ Project Roadmap

### ✅ Completed
- Created GitHub repo and uploaded datasets
- Created `scripts/embed_data.py` and embedded `alphabetical_list.csv`
- Connected OpenAI and Pinecone
- Tested embeddings via Google Colab

### 🔜 Upcoming
- [ ] Add FastAPI backend (`backend/app.py`)
- [ ] Build `/classify` endpoint using GPT-4o + Pinecone
- [ ] Add frontend UI (optional)
- [ ] Embed IPOS and USPTO datasets
- [ ] Improve system prompt for ambiguity and multi-class logic
- [ ] Prepare for public or WIPO presentation
