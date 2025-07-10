#!/usr/bin/env python3
"""
Setup script for Stock Pitch AI
Helps users get started with the project
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Set up the environment for the Stock Pitch AI project."""
    
    print("🚀 Stock Pitch AI Setup")
    print("=" * 40)
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Virtual environment not found")
        print("Please run: python -m venv venv")
        return False
    
    print("✅ Virtual environment found")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file from template...")
        
        # Copy template
        template_file = Path(".env.template")
        if template_file.exists():
            with open(template_file, 'r') as f:
                template_content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(template_content)
            
            print("✅ .env file created")
            print("⚠️  Please edit .env file and add your OpenAI API key")
        else:
            print("❌ .env.template not found")
            return False
    else:
        print("✅ .env file exists")
    
    # Check if dependencies are installed
    try:
        import streamlit
        import pandas
        import yfinance
        import openai
        print("✅ Core dependencies installed")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("\n🎉 Setup complete!")
    print("\nQuick start guide:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run: streamlit run main.py")
    print("3. Open your browser to http://localhost:8501")
    
    return True

if __name__ == "__main__":
    success = setup_environment()
    sys.exit(0 if success else 1)
