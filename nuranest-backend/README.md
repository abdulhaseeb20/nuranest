# 🏥 Nuranest Pregnancy AI API

A simplified FastAPI-based REST API for pregnancy health information using AI-powered document retrieval.

## 🚀 Quick Start

### 1. Setup (First Time Only)
```bash
cd nuranest-backend

# Run setup script
python setup.py

# Install dependencies (if needed)
pip install -r requirements.txt

# Create vectorstore from medical PDFs
python ingest_local.py
```

### 2. Start the Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📋 API Endpoints

### Ask a Pregnancy Question
```http
POST /api/v1/ai/ask
```

**Request Body:**
```json
{
  "question": "What foods should I avoid during pregnancy?"
}
```

**Response:**
```json
{
  "answer": "💡 During pregnancy, you should avoid raw fish, unpasteurized dairy products, high-mercury fish, raw eggs, and undercooked meat. 📋 Key recommendations: • Avoid raw or undercooked seafood • Stay away from unpasteurized dairy • Limit high-mercury fish consumption • Cook eggs thoroughly ⚠️ **Medical Disclaimer:** This information is for educational purposes only. Always consult with your healthcare provider for personalized medical advice.",
  "confidence_score": 0.92,
  "processing_time": 1.5,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 📝 Usage Examples

### Python
```python
import requests

response = requests.post("http://localhost:8000/api/v1/ai/ask", json={
    "question": "What are the symptoms of preeclampsia?"
})

print(response.json()["answer"])
```

### cURL
```bash
curl -X POST "http://localhost:8000/api/v1/ai/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Is it safe to exercise during pregnancy?"}'
```

## ⚙️ Configuration

### Environment Setup

1. **Copy the example environment file:**
```bash
cp env.example .env
```

2. **Edit the `.env` file and add your API key:**
```bash
nano .env
```

3. **Required Environment Variables:**
```env
# Required - Get your API key from: https://console.groq.com/
GROQ_API_KEY=your_groq_api_key_here

# Optional - Server configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false
LOG_LEVEL=INFO
```

**Note:** The `.env` file is already in `.gitignore` to keep your API keys secure.

## 🎯 Features

- ✅ **AI-powered pregnancy Q&A**
- ✅ **Evidence-based responses**
- ✅ **Medical disclaimers**
- ✅ **Clean API responses**
- ✅ **Fast processing**

## 📚 Knowledge Base

The system uses 124+ medical documents from authoritative sources:
- WHO (World Health Organization)
- NIH (National Institutes of Health)
- CDC (Centers for Disease Control)
- NHS (National Health Service)
- Mayo Clinic

## 🏗️ Architecture

- **FastAPI** - Web framework
- **Groq LLM** - Language model (Llama3-8b)
- **FAISS** - Vector database
- **Sentence Transformers** - Embeddings
- **LangChain** - AI orchestration
