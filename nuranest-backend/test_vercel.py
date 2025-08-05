#!/usr/bin/env python3
"""
Test script to verify Vercel deployment compatibility
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from app.main import app
        print("✅ FastAPI app imported successfully")
    except Exception as e:
        print(f"❌ Failed to import FastAPI app: {e}")
        return False
    
    try:
        from app.config import settings
        print("✅ Settings imported successfully")
    except Exception as e:
        print(f"❌ Failed to import settings: {e}")
        return False
    
    try:
        from app.services import pregnancy_service
        print("✅ Services imported successfully")
    except Exception as e:
        print(f"❌ Failed to import services: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variables"""
    print("\n🔧 Testing environment...")
    
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        print("✅ GROQ_API_KEY found")
    else:
        print("⚠️ GROQ_API_KEY not found (will need to be set in Vercel)")
    
    return True

def test_app_creation():
    """Test if the FastAPI app can be created"""
    print("\n🚀 Testing app creation...")
    
    try:
        from app.main import app
        print("✅ FastAPI app created successfully")
        print(f"📝 App title: {app.title}")
        print(f"📝 App version: {app.version}")
        return True
    except Exception as e:
        print(f"❌ Failed to create app: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Vercel Deployment Compatibility Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_environment,
        test_app_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("✅ All tests passed! Ready for Vercel deployment.")
        return 0
    else:
        print("❌ Some tests failed. Please fix issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 