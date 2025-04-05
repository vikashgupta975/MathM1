import streamlit as st
import os
from utils import send_to_mistral, format_response

# Page configuration
st.set_page_config(
    page_title="Math Problem Solver",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API key handling
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "yKoYjnsYQlZfIVujHW1Oh5racq98HGGJ")

# Initialize session state for chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# App header
st.title("🧮 Math Problem Solver")
st.markdown("""
This chatbot can help you solve various types of mathematical problems. 
Just describe your math problem clearly, and I'll provide a step-by-step solution.
""")

# Sidebar with information
with st.sidebar:
    st.header("About")
    st.markdown("""
    This Math Problem Solver uses Mistral AI to:
    
    - Solve algebra problems
    - Work with calculus (derivatives, integrals)
    - Solve geometry problems
    - Help with statistics and probability
    - Solve equations and systems
    - And much more!
    
    Simply type your math problem in as much detail as possible.
    """)
    
    st.header("Examples")
    st.markdown("""
    - Solve: 2x + 5 = 13
    - Find the derivative of f(x) = x² + 3x + 2
    - Calculate the area of a circle with radius 5
    - What is the probability of getting at least one head in 3 coin flips?
    - Solve the system of equations: x + y = 10, 2x - y = 5
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(message["content"], unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

# Get user input
user_input = st.chat_input("Enter your math problem here...")

# Process user input
if user_input:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display thinking indicator
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking... 🤔")
        
        try:
            # Create a math-focused prompt
            math_prompt = f"""
            You are a specialized math problem-solving assistant. Your task is to help solve the following math problem:

            {user_input}

            Please follow these guidelines:
            1. Carefully analyze the problem.
            2. Show all steps clearly.
            3. Explain your reasoning at each step.
            4. Verify your solution.
            5. Provide the final answer clearly marked.

            Focus exclusively on the mathematical problem and solution.
            """
            
            # Send to Mistral AI
            response = send_to_mistral(math_prompt, MISTRAL_API_KEY)
            
            # Format response for better readability
            formatted_response = format_response(response)
            
            # Update placeholder with response
            message_placeholder.markdown(formatted_response, unsafe_allow_html=True)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": formatted_response})
            
        except Exception as e:
            error_message = f"Sorry, I encountered an error: {str(e)}"
            message_placeholder.markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
