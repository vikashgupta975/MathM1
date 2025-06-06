# Math Problem Solver Chatbot

A Streamlit-based application that uses Mistral AI to solve various types of mathematical problems with step-by-step explanations.

## Features

- Interactive chat interface for inputting math problems
- Step-by-step solutions for various types of math problems:
  - Algebra
  - Calculus (derivatives, integrals)
  - Geometry
  - Statistics and probability
  - Equations and systems
  - And more
- Chat history to review previous problems and solutions
- Clear explanations at each step of the solution process

## Setup and Running

1. Ensure you have the required packages installed:
   - streamlit
   - requests
   - markdown

2. Set the Mistral AI API key as an environment variable (or use the default key included in the app):
   ```
   export MISTRAL_API_KEY="your_api_key_here"
   ```

3. Run the application:
   ```
   streamlit run app.py
   ```

4. The application will be available at `http://localhost:5000`

## Usage

1. Enter your math problem in the chat input field
2. The chatbot will analyze your problem and provide a detailed step-by-step solution
3. You can ask follow-up questions or enter new problems
4. Use the "Clear Chat History" button in the sidebar to start a fresh conversation

## How It Works

The application sends your math problem to Mistral AI with specific prompting to focus on step-by-step mathematical solutions. The response is then formatted for readability in the Streamlit interface.

## Deploying to Streamlit Cloud

1. **Create a GitHub repository** with these files:
   - app.py
   - utils.py
   - .streamlit/config.toml (modified - see below)

2. **Modify the `.streamlit/config.toml` file** for Streamlit Cloud:
   ```toml
   [server]
   headless = true
   
   [theme]
   # Your theme settings...
   ```
   *Note: Remove the port and address settings as Streamlit Cloud manages these automatically*

3. **Create a requirements.txt file** with the following dependencies:
   ```
   streamlit>=1.24.0
   requests>=2.28.0
   markdown>=3.4.0
   ```

4. **Go to [Streamlit Cloud](https://streamlit.io/cloud)** and create an account

5. **Create a new app** by connecting to your GitHub repo

6. **Set up your Mistral API key** in Streamlit Cloud:
   - Click on "Advanced settings" 
   - Go to "Secrets"
   - Add your Mistral API key in TOML format:
   ```
   MISTRAL_API_KEY = "your-api-key-here"
   ```
   
7. **Deploy!** Your app will be available at a unique URL

## Deploying to Streamlit Cloud

1. **Create a GitHub repository** with these files:
   - app.py
   - utils.py
   - .streamlit/config.toml (modified - see below)

2. **Modify the `.streamlit/config.toml` file** for Streamlit Cloud:
   ```toml
   [server]
   headless = true
   
   [theme]
   # Your theme settings...
   ```
   *Note: Remove the port and address settings as Streamlit Cloud manages these automatically*

3. **Create a requirements.txt file** with the following dependencies:
   ```
   streamlit>=1.24.0
   requests>=2.28.0
   markdown>=3.4.0
   ```

4. **Go to [Streamlit Cloud](https://streamlit.io/cloud)** and create an account

5. **Create a new app** by connecting to your GitHub repo

6. **Set up your Mistral API key** in Streamlit Cloud:
   - Click on "Advanced settings" 
   - Go to "Secrets"
   - Add your Mistral API key in TOML format:
   ```
   MISTRAL_API_KEY = "your-api-key-here"
   ```
   
7. **Deploy!** Your app will be available at a unique URL

## Streamlit Cloud Deployment

For easy deployment to Streamlit Cloud, check the `deploy` directory which contains:

- Deployment-optimized `.streamlit/config.toml` without port/address settings
- Ready-to-use `requirements.txt` file
- Detailed deployment instructions

Follow the instructions in `deploy/README.md` for a step-by-step deployment guide.
