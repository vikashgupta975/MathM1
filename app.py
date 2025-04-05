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

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0

# Set the correct credentials
CORRECT_NAME = "Vikash Gupta"
CORRECT_REG_NO = "12321380"

# Login Page
if not st.session_state.logged_in:
    st.title("🔐 Login to Math Problem Solver")
    
    # More professional login page
    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #1E88E5;">Welcome to Math Problem Solver</h3>
        <p>Please log in with your credentials to access the application</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form with username and password instead
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            # Still use the same values, but as username/password instead
            if username == CORRECT_NAME and password == CORRECT_REG_NO:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.session_state.login_attempts += 1
                st.error(f"Invalid credentials. Please try again. ({st.session_state.login_attempts} attempts)")
                
    # Add a hint about credentials in a less obvious way
    with st.expander("Need help logging in?"):
        st.info("Contact your administrator or instructor if you forgot your login credentials.")
        
    # Creator information in small text at the bottom
    st.markdown("""
    <div style="position: fixed; bottom: 10px; right: 10px; text-align: right; opacity: 0.7; font-size: 12px;">
        <p style="margin: 0; padding: 0;">Creator: Vikash Gupta</p>
        <p style="margin: 0; padding: 0;">Reg. No: 12321380</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Main App header
    st.title("🧮 Math Problem Solver")
    st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
        <p><strong>Welcome back!</strong> You are now logged in and can use the Math Problem Solver.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    This chatbot can help you solve various types of mathematical problems. 
    Just describe your math problem clearly, and I'll provide a step-by-step solution.
    """)
    
    # Creator information in small text at the bottom
    st.markdown("""
    <div style="position: fixed; bottom: 10px; right: 10px; text-align: right; opacity: 0.7; font-size: 12px;">
        <p style="margin: 0; padding: 0;">Creator: Vikash Gupta</p>
        <p style="margin: 0; padding: 0;">Reg. No: 12321380</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    if st.session_state.logged_in:
        st.header("Account")
        st.markdown(f"""
        **Status:** Logged in
        **User:** {CORRECT_NAME}
        """)
        
        # Logout button at the top of sidebar
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    
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
    
    if st.session_state.logged_in and st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Only show chat interface when logged in
if st.session_state.logged_in:
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
else:
    # If not logged in, show a message about needing to log in
    st.info("Please log in to use the Math Problem Solver.")
