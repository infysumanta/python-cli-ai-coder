"""
Entry point for the Python CLI AI Coder.

This is the main entry point for the application that generates complete project
structures based on user specifications. The tool provides an interactive CLI
interface for selecting project types, features, and configurations.

Requirements:
    - Python 3.8+
    - OpenAI API key (set in .env file)
    - Virtual environment (recommended)

Before running:
    1. Make sure to activate the virtual environment:
       source .venv/bin/activate  # On Unix/Mac
       .venv/Scripts/activate     # On Windows

    2. Ensure your .env file contains your OpenAI API key:
       OPENAI_API_KEY=your_api_key_here

Usage:
    python main.py
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def is_venv():
    """Check if the application is running in a virtual environment.

    Returns:
        bool: True if running in a virtual environment, False otherwise
    """
    return hasattr(sys, 'real_prefix') or \
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

# Import the main CLI function
from src.cli.main import main

if __name__ == "__main__":
    if not is_venv():
        print("\033[93mWarning: It's recommended to run this application in the virtual environment.\033[0m")
        print("To activate the virtual environment:")
        print("  source .venv/bin/activate  # On Unix/Mac")
        print("  .venv/Scripts/activate     # On Windows")
        print("\nContinuing without virtual environment...\n")

    main()