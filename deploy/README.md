# Streamlit Cloud Deployment Guide

This guide provides step-by-step instructions for deploying this Math Problem Solver application to Streamlit Cloud.

## Prerequisites

1. A Streamlit Cloud account (sign up at [https://share.streamlit.io/](https://share.streamlit.io/))
2. A GitHub repository with your application
3. A Mistral AI API key (sign up at [https://mistral.ai/](https://mistral.ai/))

## Deployment Steps

### 1. Push your code to GitHub

Make sure your repository includes these files:
- `app.py` - Your main application file
- `utils.py` - Utility functions
- `.streamlit/config.toml` from this deploy folder
- `requirements.txt` from this deploy folder

### 2. Configure Streamlit Cloud Secrets

1. In your Streamlit Cloud dashboard, select your app
2. Click on "Advanced Settings" > "Secrets"
3. Add your Mistral AI API key in TOML format:

```toml
MISTRAL_API_KEY = "your-mistral-api-key-here"
```

### 3. Deploy on Streamlit Cloud

1. Connect your GitHub repository
2. Select the repository and branch
3. Set the main file path to: `app.py`
4. Click "Deploy"

### 4. Fixing "Health Check" Errors

If you encounter health check errors during deployment:

1. Use the `.streamlit/config.toml` file from this deploy folder (without port specification)
2. Make sure you're not hardcoding the port in your application
3. Let Streamlit Cloud handle the port assignment

### Updating Your Deployment

When making changes to your app:
1. Push changes to your GitHub repository
2. Streamlit Cloud will automatically redeploy your app

### Project Information

- **Creator**: Vikash Gupta (Reg. No. 12321380)
- **API**: Mistral AI
- **Framework**: Streamlit