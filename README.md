## NuraNest - Redefining Women Pregnancy Healthcare

## 🌐 Phase 1: Research & Planning
🔹 Goals:
Define the scope and features of Nuranest.<br>


Understand the clinical use cases and risk factors (e.g., preeclampsia, gestational diabetes).<br>


🔹 Actions:<br>
Consult OB-GYN professionals or use guidelines (e.g., WHO, ACOG).<br>


Create user personas: first-time mothers, high-risk pregnancies, etc.<br>


Identify what symptoms the bot should assess (fatigue, swelling, bleeding, etc.).<br>


Create a dataset plan: structured (symptom-risk mapping) and unstructured (medical documents).<br>



## 📦 Phase 2: Data Collection & Curation
🔹 Goals:<br>
Build your corpus for Retrieval.<br>
🔹 Sources:<br>
WHO Pregnancy Guidelines<br>


NIH MedlinePlus / PubMed<br>


Mayo Clinic, ACOG papers<br>


Pregnancy symptom checklists<br>


Risk assessment tools (Bishop Score, GDM calculators)<br>


🔹 Actions:
Convert PDFs to text using OCR.<br>


Segment data by topics (nutrition, symptoms, trimesters).<br>


Store in a vectorized document store (FAISS).<br>



## 🧠 Phase 3: Model Design — RAG Chatbot
🔹 Architecture:<br>
Retriever: Retrieves relevant docs from the vector store.<br>


Generator: Uses LLM (LLaMA) to generate answers.<br>


🔹 Tools:
Embeddings:  Hugging Face (Instructor XL)<br>


Vector Store: FAISS<br>


LLM: OpenAI, LLaMA-3<br>


Frameworks: LlamaIndex for chaining<br>


🔹 Flow:<br>
User enters symptoms (e.g., "swelling in legs and headaches").<br>


Bot parses query → gets embeddings.<br>


Query goes to vector DB → returns relevant chunks.<br>


LLM receives context and user query → returns answer.<br>



## 💬 Phase 4: Symptom Intake & Risk Assessment Logic
🔹 Symptom Collection:<br>
Guided conversation with structured prompts (form-based or open chat).<br>


Use classification or NLP tagging to normalize inputs (e.g., “I feel dizzy” → dizziness).<br>


🔹 Risk Analysis:<br>
Rule-based mapping (initially): “swelling + headaches + vision issues → possible preeclampsia”.<br>


Later: use probabilistic scoring or train a shallow ML model.<br>


🔹 Risk Levels:<br>
Green (Low)<br>


Yellow (Moderate, observe)<br>


Red (High, seek doctor immediately)<br>



## 🧪 Phase 5: Testing & Evaluation
🔹 Internal Testing:<br>
Simulate various symptom scenarios and assess the chatbot’s accuracy.<br>


Clinical review by experts (OB-GYN).<br>


🔹 Metrics:<br>
Precision/recall on document retrieval.<br>


Factual accuracy (human-in-the-loop review).<br>


User satisfaction scores.<br>



## 💻 Phase 6: Frontend Development
🔹 Web/Mobile UI:
Use React for cross-platform app.<br>


Symptom input interface (form & chat).<br>


Output risk levels, charts, educational tips.<br>


Track user history securely.<br>


🔹 Backend:
Use FastAPI<br>


Host RAG pipeline as an API<br>


Secure endpoints (JWT, OAuth2)<br>



## ☁️ Phase 7: Deployment & Scaling
🔹 Hosting:
Uses HuggingFace Spaces<br>

Vector DB managed FAISS<br>


🔹 CI/CD:
Use GitHub Actions or GitLab CI<br>


Dockerize services<br>


Monitor logs and user sessions<br>



## 🔒 Phase 8: Compliance, Ethics & Privacy
🔹 Data Handling:
Store no PII or use local-only modes.


Offer clear disclaimers: "Not a replacement for professional medical advice."


🔹 Certifications (optional):
HIPAA-compliant cloud


IRB clearance (if doing trials)



## 🚀 Tools Stack Summary:
## Category        Tool(s)
Embeddings:         HuggingFace Transformers<br>
Vector DB:          FAISS<br>
LLM:                LLaMA<br>
Framework:          LlamaIndex<br>
Frontend:           React.js<br>
Backend:            FastAPI<br>
Hosting:            HuggingFace Spaces<br>


