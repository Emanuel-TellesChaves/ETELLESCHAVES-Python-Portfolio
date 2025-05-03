#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Portfolio Analyzer Launcher

This script launches the Portfolio Analyzer Streamlit application.
Simply run this file and the application will start in your browser.
"""

import os
import subprocess
import sys

def main():
    """Launch the Portfolio Analyzer Streamlit application."""
    try:
        # Get the directory containing this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Path to the portfolio_analyzer.py file
        app_path = os.path.join(script_dir, "src", "portfolio_analyzer.py")
        
        # Check if the file exists
        if not os.path.exists(app_path):
            print(f"Error: Could not find {app_path}")
            return 1
        
        # Launch Streamlit with the app
        cmd = [sys.executable, "-m", "streamlit", "run", app_path]
        print(f"Starting Portfolio Analyzer: {' '.join(cmd)}")
        
        # Use subprocess to run the command
        subprocess.run(cmd)
        return 0
    
    except Exception as e:
        print(f"Error launching Portfolio Analyzer: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 