from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directory where PDFs are stored
pdf_folder = "medical_data"

def ingest_pdfs_local():
    """Ingest PDFs and create vectorstore using free local embeddings"""
    logger.info("🚀 Starting PDF ingestion with local embeddings...")
    
    # Check if folder exists
    if not os.path.exists(pdf_folder):
        raise FileNotFoundError(f"PDF folder '{pdf_folder}' not found")
    
    # Step 1: Load all PDFs
    logger.info("📄 Loading PDFs...")
    docs = []
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
    
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in '{pdf_folder}'")
    
    logger.info(f"Found {len(pdf_files)} PDF files")
    
    for filename in pdf_files:
        try:
            file_path = os.path.join(pdf_folder, filename)
            logger.info(f"Loading: {filename}")
            loader = PyPDFLoader(file_path)
            docs.extend(loader.load())
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
            continue
    
    if not docs:
        raise ValueError("No documents loaded from PDFs")
    
    logger.info(f"✅ Loaded {len(docs)} documents from PDFs")
    
    # Step 2: Split into chunks
    logger.info("✂️ Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(docs)
    
    logger.info(f"✅ Created {len(chunks)} chunks")
    
    # Step 3: Generate embeddings using free local model
    logger.info("🔍 Generating embeddings with free local model...")
    logger.info("📥 Downloading embedding model (this may take a few minutes)...")
    
    # Use a lightweight, free embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},  # Use CPU to avoid GPU requirements
        encode_kwargs={'normalize_embeddings': True}
    )
    
    logger.info("✅ Embedding model loaded successfully")
    
    # Step 4: Create vectorstore directly (simpler approach)
    logger.info("💾 Creating FAISS vectorstore...")
    
    # Create vectorstore directly - this handles embeddings automatically
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Save vectorstore
    logger.info("💾 Saving vectorstore...")
    vectorstore.save_local("vectorstore_local")
    
    logger.info("✅ Ingestion complete! Vectorstore saved to 'vectorstore_local' directory")
    
    # Print summary
    print(f"\n🎉 PDF Ingestion Summary (Local Embeddings):")
    print(f"📄 PDFs processed: {len(pdf_files)}")
    print(f"📝 Documents loaded: {len(docs)}")
    print(f"✂️ Chunks created: {len(chunks)}")
    print(f"🔍 Embeddings generated: {len(chunks)}")
    print(f"💾 Vectorstore saved to: vectorstore_local/")
    print(f"💰 Cost: FREE (no API charges)")
    
    return vectorstore

if __name__ == "__main__":
    try:
        vectorstore = ingest_pdfs_local()
        print("\n✅ Ready to use your pregnancy AI RAG system with free local embeddings!")
        print("💡 Note: Local embeddings may be slightly less accurate than OpenAI, but they're free!")
    except Exception as e:
        logger.error(f"❌ Ingestion failed: {e}")
        raise 