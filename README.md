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
