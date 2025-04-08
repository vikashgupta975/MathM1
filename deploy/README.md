# Streamlit Cloud Deployment Files

This directory contains the configuration files optimized for deploying to Streamlit Cloud.

## Deployment Instructions

1. **Create a GitHub repository** with the following files:
   - Copy the main files from your project:
     - `app.py`
     - `utils.py`
   - Use the `.streamlit/config.toml` from this directory (has port/address settings removed)
   - Create a `requirements.txt` file with:
     ```
     streamlit>=1.24.0
     requests>=2.28.0
     markdown>=3.4.0
     ```

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)** and create an account

3. **Create a new app** by connecting to your GitHub repo

4. **Set up your Mistral API key** in Streamlit Cloud:
   - Click on "Advanced settings" 
   - Go to "Secrets"
   - Add your Mistral API key in TOML format:
   ```
   MISTRAL_API_KEY = "your-api-key-here"
   ```
   
5. **Deploy!** Your app will be available at a unique URL

## Important Notes

- The configuration in this directory has the port and address settings removed, as Streamlit Cloud manages these automatically
- Make sure to add your Mistral API key to the Secrets section in Streamlit Cloud
- Do not include the default API key in your deployed code for security reasons