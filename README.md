# 🎯 NICE Classification Assistant (AI + RAG)

**An AI-powered assistant that helps classify goods and services using NICE classification data from IPOS, USPTO and official guidelines.**  
Built with OpenAI, Pinecone, and fully open-source.

---

## ✨ What It Does

🔍 Ask: _“Where should I classify Bluetooth-connected aroma diffusers?”_  
🧠 It searches your real classification data (IPOS, USPTO, alphabetical list)  
💬 Then GPT-4o answers like an expert, with justification and context

---

## 🧠 Powered by:
- **OpenAI GPT-4o** for smart answers and embeddings
- **Pinecone** for fast vector search (RAG retrieval)
- **Your own classification data** (up to 200,000+ terms)
- **FastAPI** backend + optional frontend UI

---

## 📦 Key Features
- 💡 Understands unknown, vague, or multi-class terms
- 🧾 Justifies answers with real NICE classification context
- 🔧 Easy to update (just add new data)
- 🌍 Fully online (Colab + GitHub + Pinecone)
- 📖 Open-source (GPLv3)

---

## 🚀 Demo Ready
Use your own dataset. Embed it in Colab. Deploy with one command.  
Then ask real-world questions — in English, French, or Spanish — and get expert-level classification help.

---

## 🔗 Quick Links
- [Project Summary](nice-classification-summary.md)
- [Roadmap](nice-classification-roadmap.md)
- [Architecture Explained](nice-classification-architecture-explained.md)

> Built by [punkinet](https://github.com/punkinet) — inspired by real-world NICE classification needs.

---

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
