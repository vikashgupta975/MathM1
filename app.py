import streamlit as st
import os
import streamlit.components.v1 as components
from utils import send_to_mistral, format_response

# Page configuration
st.set_page_config(
    page_title="Math Problem Solver",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* General styling */
    body {
        font-family: 'Inter', sans-serif;
    }
    
    .math-problem {
        background-color: #f8f9fa;
        border-left: 5px solid #1E88E5;
        padding: 15px;
        border-radius: 12px;
        margin: 18px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .solution-step {
        margin: 18px 0;
        padding: 15px;
        border-radius: 12px;
        background-color: #f0f2f6;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .final-answer {
        background-color: #e8f4f8;
        border-radius: 12px;
        padding: 18px;
        margin: 24px 0;
        border-left: 5px solid #4CAF50;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    /* Chat message styling */
    .chat-message-user {
        padding: 12px 18px;
        border-radius: 20px 20px 4px 20px;
        margin: 12px 0;
        display: inline-block;
        background-color: #f0f2f6;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        border-bottom: 2px solid #1E88E5;
        max-width: 85%;
    }
    
    .chat-message-assistant {
        padding: 12px 18px;
        border-radius: 20px 20px 20px 4px;
        margin: 12px 0;
        display: inline-block;
        background-color: #e8f4f8;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        border-bottom: 2px solid #4CAF50;
        max-width: 85%;
    }
    
    /* App transition effects */
    .stApp {
        transition: all 0.3s ease;
    }
    
    /* Branding header */
    .branding-header {
        background: linear-gradient(135deg, #1E88E5, #0D47A1);
        color: white;
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .branding-header h2 {
        margin: 0;
        font-weight: 600;
    }
    
    .creator-badge {
        background-color: rgba(255,255,255,0.15);
        padding: 8px 12px;
        border-radius: 30px;
        font-size: 14px;
        display: inline-block;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 10px;
        transition: all 0.2s ease;
        font-weight: 500;
        padding: 4px 8px;
        border: none;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        transition: all 0.2s ease;
        padding: 8px 12px;
        border: 1px solid #ddd;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1E88E5;
        box-shadow: 0 0 0 2px rgba(30,136,229,0.2);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        border-right: 1px solid #eaeaea;
    }
    
    /* Theme toggle buttons */
    .theme-toggle-light {
        background-color: #ffeb3b !important;
        color: #333 !important;
    }
    
    .theme-toggle-dark {
        background-color: #3f51b5 !important;
        color: white !important;
    }
    
    /* Dark mode styles */
    body.dark {
        color: #f0f2f6;
        background-color: #1a1a1a;
    }
    
    body.dark .stTextInput > div > div > input {
        background-color: #333;
        color: white;
        border-color: #555;
    }
    
    body.dark .solution-step {
        background-color: #333;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    body.dark .math-problem {
        background-color: #333;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    body.dark .final-answer {
        background-color: #2e4b38;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    body.dark .chat-message-user {
        background-color: #333;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        border-bottom: 2px solid #64b5f6;
    }
    
    body.dark .chat-message-assistant {
        background-color: #1e3a47;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        border-bottom: 2px solid #66bb6a;
    }
    
    body.dark .stButton button {
        background-color: #444;
        color: white;
    }
    
    body.dark .sidebar .sidebar-content {
        background-color: #262626;
        border-right: 1px solid #333;
    }
    
    body.dark .branding-header {
        background: linear-gradient(135deg, #0D47A1, #1a237e);
    }
    
    /* Creator info styling */
    .creator-info {
        position: fixed;
        bottom: 10px;
        right: 10px;
        text-align: right;
        font-size: 13px;
        transition: all 0.3s ease;
        background-color: rgba(255,255,255,0.1);
        padding: 8px 12px;
        border-radius: 30px;
        backdrop-filter: blur(5px);
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .creator-info:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Code blocks styling */
    pre {
        border-radius: 8px;
        padding: 15px;
        background-color: #f5f5f5;
        overflow-x: auto;
    }
    
    body.dark pre {
        background-color: #2d2d2d;
    }
    
    /* Equations styling */
    .equation {
        padding: 10px;
        background-color: #f9f9f9;
        border-radius: 8px;
        overflow-x: auto;
        margin: 10px 0;
    }
    
    body.dark .equation {
        background-color: #333;
    }
    
    /* Thinking animation */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .thinking-animation {
        animation: pulse 1.5s infinite ease-in-out;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# API key handling
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "yKoYjnsYQlZfIVujHW1Oh5racq98HGGJ")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0
    
if "theme" not in st.session_state:
    st.session_state.theme = "light"  # Default theme

# Set the correct credentials
CORRECT_NAME = "Vikash Gupta"
CORRECT_REG_NO = "12321380"

# Login Page
if not st.session_state.logged_in:
    # Branded login header
    st.markdown("""
    <div class="branding-header">
        <div>
            <h2>🔐 Math Problem Solver Login</h2>
            <p style="margin: 5px 0 0 0;">Powered by Mistral AI</p>
        </div>
        <div class="creator-badge">
            <span>Created by: Vikash Gupta | Reg No: 12321380</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # More professional login page with dark mode compatibility
    if st.session_state.theme == "dark":
        bg_color = "#3b3b40"
        card_border = "1px solid #555"
    else:
        bg_color = "#f0f2f6"
        card_border = "1px solid #eaeaea"
        
    st.markdown(f"""
    <div style="background-color: {bg_color}; padding: 25px; border-radius: 12px; margin: 20px 0; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.1); transition: all 0.3s ease; 
            border: {card_border};">
        <h3 style="color: #1E88E5; margin-top: 0;">Welcome to Math Problem Solver!</h3>
        <p style="margin-bottom: 20px;">Please log in with your credentials to access the application.</p>
        <p style="font-size: 14px; opacity: 0.8; margin-top: 10px;">This secure interface provides access to a powerful math problem-solving assistant powered by Mistral AI.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form with username and password
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form", border=False):
            # Style the form with custom CSS
            st.markdown("""
            <style>
                div[data-testid="stForm"] {
                    background-color: white;
                    padding: 20px;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                    border: 1px solid #eaeaea;
                }
                
                body.dark div[data-testid="stForm"] {
                    background-color: #2d2d2d;
                    border: 1px solid #444;
                }
            </style>
            """, unsafe_allow_html=True)
            
            st.subheader("Account Login")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            # Make submit button more prominent
            submit_button = st.form_submit_button("Login", use_container_width=True)
            
            if submit_button:
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
    <div class="creator-info">
        <p style="margin: 0; padding: 0;">Creator: Vikash Gupta</p>
        <p style="margin: 0; padding: 0;">Reg. No: 12321380</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Main App header with branding
    st.markdown("""
    <div class="branding-header">
        <div>
            <h2>🧮 Math Problem Solver</h2>
            <p style="margin: 5px 0 0 0;">Powered by Mistral AI</p>
        </div>
        <div class="creator-badge">
            <span>Created by: Vikash Gupta | Reg No: 12321380</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message with dark mode compatibility
    if st.session_state.theme == "dark":
        bg_color = "#3b3b40"
    else:
        bg_color = "#f0f2f6"
        
    st.markdown(f"""
    <div style="background-color: {bg_color}; padding: 15px; border-radius: 12px; margin-bottom: 20px; 
               box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: all 0.3s ease;">
        <p><strong>Welcome back!</strong> You are now logged in and can use the Math Problem Solver.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    This chatbot can help you solve various types of mathematical problems. 
    Just describe your math problem clearly, and I'll provide a step-by-step solution.
    """)
    
    # Creator information in small text at the bottom
    st.markdown("""
    <div class="creator-info">
        <p style="margin: 0; padding: 0;">Creator: Vikash Gupta</p>
        <p style="margin: 0; padding: 0;">Reg. No: 12321380</p>
    </div>
    """, unsafe_allow_html=True)

# Apply dark mode if enabled
if st.session_state.theme == "dark":
    st.markdown("""
    <script>
        document.body.classList.add('dark');
        document.getElementsByTagName('html')[0].style.backgroundColor = '#262730';
    </script>
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
        
        # Enhanced theme toggle
        st.write("### Appearance")
        
        # Custom CSS for theme toggle buttons
        st.markdown("""
        <style>
            .theme-toggle-container {
                display: flex;
                gap: 10px;
                margin-top: 10px;
                margin-bottom: 20px;
            }
            
            .theme-button {
                flex: 1;
                text-align: center;
                padding: 10px;
                border-radius: 10px;
                cursor: pointer;
                transition: all 0.3s ease;
                user-select: none;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            
            .light-button {
                background-color: #f5f5f5;
                color: #333;
                border: 1px solid #ddd;
            }
            
            .dark-button {
                background-color: #333;
                color: #fff;
                border: 1px solid #555;
            }
            
            .active-theme {
                transform: scale(1.05);
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                font-weight: bold;
            }
            
            .light-button.active-theme {
                border: 2px solid #ffeb3b;
            }
            
            .dark-button.active-theme {
                border: 2px solid #5c6bc0;
            }
            
            body.dark .light-button {
                background-color: #444;
                color: #f5f5f5;
                border: 1px solid #666;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Create interactive theme buttons with JavaScript
        theme_col1, theme_col2 = st.columns(2)
        
        with theme_col1:
            light_active = "active-theme" if st.session_state.theme == "light" else ""
            if st.button("🌞 Light Mode", key="light_mode", disabled=st.session_state.theme == "light"):
                st.session_state.theme = "light"
                st.rerun()
                
        with theme_col2:
            dark_active = "active-theme" if st.session_state.theme == "dark" else ""
            if st.button("🌙 Dark Mode", key="dark_mode", disabled=st.session_state.theme == "dark"):
                st.session_state.theme = "dark"
                st.rerun()
        
        # Theme is applied globally
    
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

    # Add some space before the input field
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    
    # Style the chat input
    st.markdown("""
    <style>
        /* Chat input styling */
        .stChatInputContainer {
            padding: 10px;
            border-radius: 12px;
            background-color: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(6px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        body.dark .stChatInputContainer {
            background-color: rgba(59, 59, 64, 0.3);
        }
        
        .stChatInputContainer:hover {
            box-shadow: 0 6px 16px rgba(0,0,0,0.15);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Get user input with a more descriptive placeholder
    user_input = st.chat_input("Type your math problem here and press Enter...")

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
            message_placeholder.markdown("<div class='thinking-animation'>Solving your math problem... <span>🧮</span><span>📊</span><span>📈</span></div>", unsafe_allow_html=True)
            
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
