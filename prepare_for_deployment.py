#!/usr/bin/env python3
"""
Deployment preparation script for Math Problem Solver.
This script prepares your Streamlit app for deployment by updating the config file.
"""

import os
import shutil
import sys

def prepare_for_deployment():
    """Prepare the application for deployment by updating the config file"""
    print("\n🚀 Preparing Math Problem Solver for deployment...")
    
    # Check if .streamlit directory exists
    if not os.path.exists(".streamlit"):
        print("❌ Error: .streamlit directory not found!")
        return False
    
    # Backup the original config file
    config_path = ".streamlit/config.toml"
    backup_path = ".streamlit/config.toml.bak"
    
    if os.path.exists(config_path):
        print("📋 Backing up original config file...")
        shutil.copy(config_path, backup_path)
        print("✅ Backup created at: " + backup_path)
    
    # Check if deployment config exists
    deployment_config = ".streamlit/deployment-config.toml"
    if os.path.exists(deployment_config):
        print("📋 Using prepared deployment config...")
        shutil.copy(deployment_config, config_path)
    else:
        # Create a new config without port specification
        print("📋 Creating new deployment config...")
        with open(config_path, "w") as f:
            f.write("""[server]
headless = true
# Note: Port and address removed for cloud deployment

[theme]
# Base theme is light
primaryColor = "#1E88E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
""")
    
    print("✅ Config file updated for deployment!")
    print("\n📝 IMPORTANT DEPLOYMENT STEPS:")
    print("1. Commit these changes to your GitHub repository")
    print("2. Go to Streamlit Cloud: https://share.streamlit.io/")
    print("3. Connect your GitHub repository")
    print("4. Set the main file path to: app.py")
    print("5. In Advanced Settings > Secrets, add your Mistral API key:")
    print("   MISTRAL_API_KEY = \"your-key-here\"")
    print("6. Click Deploy")
    print("\n🎉 Your Math Problem Solver will be available online shortly!")
    return True

if __name__ == "__main__":
    prepare_for_deployment()