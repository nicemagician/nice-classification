# 🎯 Nice Classification Assistant (AI + RAG)

**An AI-powered assistant that helps classify goods and services using official WIPO NICE classification sources — starting with the Alphabetical List, and soon other Madrid-related data.**  
Built with OpenAI, Pinecone, and fully open-source.

---

## ✨ What It Does

🔍 Ask: _“Where should I classify Bluetooth-connected aroma diffusers?”_  
🧠 It searches your official classification data (e.g. WIPO Alphabetical List)  
💬 Then GPT-4o answers like an expert, with justification and context

---

## 🧠 Powered by:
- **OpenAI GPT-4o** for smart answers and embeddings
- **Pinecone** for fast vector search (RAG retrieval)
- **Your own WIPO classification data** (e.g. Alphabetical List)
- **FastAPI** backend + modern frontend UI

---

## 📦 Key Features
- 💡 Understands unknown, vague, or multi-class terms
- 🧾 Justifies answers with real NICE classification context
- 🔧 Easy to update (just add new data)
- 🌍 Fully online (Replit + GitHub + Vercel + Pinecone)
- 📖 Open-source (GPLv3)

---

## 🚀 Demo Ready
Use your own dataset. Deploy in minutes.  
Then ask real-world questions — in English, French, or Spanish — and get expert-level classification help.

---

## 🔗 Quick Links
- [Project Summary](nice-classification-summary.md)
- [Roadmap](nice-classification-roadmap.md)
- [Architecture Explained](nice-classification-architecture-explained.md)

> Built by [punkinet](https://github.com/punkinet) — focused 100% on WIPO-based classification.

---

## 🔧 Setup Instructions
1. Clone the repo
2. Put your classification data into `data/`
3. Set API keys in `.env`
4. Run `scripts/embed_data.py` to index your data
5. Start the API with `uvicorn backend.app:app --reload` or deploy via Replit

---

## 🌍 Deployment
- Use Vercel for frontend
- Use Replit Reserved VM for backend
- Use Pinecone for vector DB

---

## 📦 .env.example
```env
OPENAI_API_KEY=your_openai_key_here
PINECONE_API_KEY=your_pinecone_key_here
PINECONE_INDEX=nice-classification
```

---

## 🗺️ Project Roadmap

### ✅ Completed
- Created GitHub repo and uploaded Alphabetical List
- Created `scripts/embed_data.py` and embedded data
- Connected OpenAI and Pinecone
- Set up FastAPI backend on Replit
- Deployed frontend with Vercel
- Deployed backend on Reserved VM with auto-restart via `main.py`

### 🔜 Upcoming
- [ ] Add MGS, XMASTree and Madrid Guidelines
- [ ] Improve multilingual prompt logic
- [ ] Prepare demo for internal/external showcase
