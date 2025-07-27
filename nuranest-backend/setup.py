#!/usr/bin/env python3
"""
Setup script for Nuranest Pregnancy AI API
"""

import os
import shutil
import subprocess
import sys

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def setup_environment():
    """Setup environment file"""
    if not os.path.exists('.env'):
        if os.path.exists('env.example'):
            shutil.copy('env.example', '.env')
            print("✅ Created .env file from env.example")
            print("📝 Please edit .env and add your GROQ_API_KEY")
        else:
            print("⚠️ env.example not found, creating basic .env file")
            with open('.env', 'w') as f:
                f.write("# Nuranest Pregnancy AI API Environment\n")
                f.write("# Add your API key below:\n")
                f.write("GROQ_API_KEY=your_groq_api_key_here\n")
                f.write("HOST=0.0.0.0\n")
                f.write("PORT=8000\n")
                f.write("DEBUG=false\n")
                f.write("LOG_LEVEL=INFO\n")
            print("✅ Created basic .env file")
    else:
        print("✅ .env file already exists")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import pydantic
        import pydantic_settings
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Install dependencies with: pip install -r requirements.txt")
        return False

def check_vectorstore():
    """Check if vectorstore exists"""
    if os.path.exists('vectorstore_local'):
        print("✅ Vectorstore found")
        return True
    else:
        print("⚠️ Vectorstore not found")
        print("💡 Run: python ingest_local.py to create vectorstore from medical PDFs")
        return False

def main():
    """Main setup function"""
    print("🏥 Nuranest Pregnancy AI API Setup")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Setup environment
    setup_environment()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Check vectorstore
    vectorstore_ok = check_vectorstore()
    
    print("\n" + "=" * 50)
    print("📋 Setup Summary:")
    print(f"✅ Environment: {'Ready' if os.path.exists('.env') else 'Needs setup'}")
    print(f"✅ Dependencies: {'Installed' if deps_ok else 'Need installation'}")
    print(f"✅ Vectorstore: {'Found' if vectorstore_ok else 'Needs creation'}")
    
    print("\n🚀 Next Steps:")
    if not deps_ok:
        print("1. Install dependencies: pip install -r requirements.txt")
    if not os.path.exists('.env') or 'your_groq_api_key_here' in open('.env').read():
        print("2. Edit .env file and add your GROQ_API_KEY")
    if not vectorstore_ok:
        print("3. Create vectorstore: python ingest_local.py")
    print("4. Start the server: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    print("5. Access API docs: http://localhost:8000/docs")
    
    print("\n✅ Setup complete!")

if __name__ == "__main__":
    main() 