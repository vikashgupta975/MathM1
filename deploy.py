#!/usr/bin/env python3
"""
Streamlit Cloud Deployment Helper
This script ensures your app is properly configured for Streamlit Cloud deployment
by removing any port settings that could cause health check errors.
"""

import os
import shutil
import sys

def prepare_for_streamlit_cloud():
    """
    Prepares the application for Streamlit Cloud deployment by
    making sure no port is specified in the config.
    """
    print("\n🚀 Preparing Math Problem Solver for Streamlit Cloud deployment...")
    
    # Ensure .streamlit directory exists
    os.makedirs(".streamlit", exist_ok=True)
    
    # Create deployment-ready config
    config_path = ".streamlit/config.toml"
    with open(config_path, "w") as f:
        f.write("""[server]
headless = true
# Note: DO NOT specify port for cloud deployment
""")
    
    print("✅ Created deployment-ready config file")
    print("\n📋 DEPLOYMENT INSTRUCTIONS:")
    print("1. Push these changes to your GitHub repository")
    print("2. Go to Streamlit Cloud: https://share.streamlit.io/")
    print("3. Connect your GitHub repository")
    print("4. Use main file path: app.py")
    print("5. In Advanced Settings > Secrets, add your Mistral API key:")
    print("   MISTRAL_API_KEY = \"your-key-here\"")
    print("6. Click Deploy")
    print("\n✨ Your app will be deployed without the port conflict error!")

if __name__ == "__main__":
    prepare_for_streamlit_cloud()