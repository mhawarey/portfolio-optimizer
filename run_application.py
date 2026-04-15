#!/usr/bin/env python3
# run_application.py - Script to run the Portfolio Optimizer application

import sys
import os

# Create necessary directories if they don't exist
os.makedirs("ui", exist_ok=True)
os.makedirs("models", exist_ok=True)
os.makedirs("utils", exist_ok=True)

# Import the main module and run the application
from main import main

if __name__ == "__main__":
    main()