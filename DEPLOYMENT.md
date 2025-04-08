# Easy Deployment Guide for Math Problem Solver

This guide provides the simplest way to deploy your Math Problem Solver application to Streamlit Cloud.

## Step 1: Clone Your GitHub Repository
Make sure your GitHub repository is up-to-date with all your code.

## Step 2: Update Configuration

### Option 1: Remove port settings (Preferred method)
In your GitHub repository, edit the `.streamlit/config.toml` file to remove the port settings:

```toml
[server]
headless = true
# Port and address removed for deployment

[theme]
# Your theme settings...
```

### Option 2: Use port 8501 (Alternative method)
Edit `.streamlit/config.toml` to use port 8501 instead of 5000:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 8501
```

## Step 3: Deploy to Streamlit Cloud

1. Go to [Streamlit Cloud](https://share.streamlit.io/)
2. Connect your GitHub repository
3. Set the main file path to: `app.py`
4. In **Advanced Settings** > **Secrets**, add your Mistral API key:
   ```toml
   MISTRAL_API_KEY = "yKoYjnsYQlZfIVujHW1Oh5racq98HGGJ"
   ```
5. Click **Deploy**

## Important Notes

* **API Key**: The app will look for your Mistral API key in this order:
  1. Streamlit secrets (added in Step 3.4)
  2. Environment variables
  3. Default key (already in the code for development)

* **Health Check Error**: If you encounter the error `checking the health of the Streamlit app: Get "http://localhost:8501/healthz": dial tcp 127.0.0.1:8501: connect: connection refused`, it means your app is trying to run on a different port than the health check expects. Follow Step 2 to fix this.

## Project Information
- **Creator**: Vikash Gupta (Reg. No. 12321380)
- **API**: Mistral AI
- **Framework**: Streamlit