"""Entry point for the Code Project Generator.

NOTE: This application requires a virtual environment.
Before running, make sure to activate the virtual environment:

    source .venv/bin/activate  # On Unix/Mac
    .venv/Scripts/activate     # On Windows

Then run the application with:
    python main.py
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if running in virtual environment
def is_venv():
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