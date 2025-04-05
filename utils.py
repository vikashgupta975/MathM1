import requests
import re
import json
import markdown

def send_to_mistral(prompt, api_key):
    """
    Send a prompt to Mistral AI API and get the response
    
    Args:
        prompt (str): The math problem prompt
        api_key (str): Mistral AI API key
    
    Returns:
        str: The response from Mistral AI
    """
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "mistral-medium",  # Using Mistral's medium model for better math capabilities
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,  # Lower temperature for more precise math solutions
        "top_p": 0.9,
        "max_tokens": 2000  # Allowing plenty of tokens for detailed step-by-step solutions
    }
    
    try:
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the JSON response
        response_data = response.json()
        
        # Extract the assistant's message content
        assistant_message = response_data["choices"][0]["message"]["content"]
        return assistant_message
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")
    except (KeyError, IndexError) as e:
        raise Exception(f"Error parsing response: {str(e)}")
    except json.JSONDecodeError:
        raise Exception("Error decoding API response")

def format_response(response):
    """
    Format the Mistral AI response for better readability in Streamlit
    
    Args:
        response (str): Raw response from Mistral AI
    
    Returns:
        str: Formatted response with HTML/markdown enhancements
    """
    # Convert standard markdown to HTML
    html_response = markdown.markdown(response)
    
    # Enhance math expressions formatting (basic approach - proper LaTeX would require MathJax)
    # Find inline math expressions wrapped in $...$ and highlight them
    html_response = re.sub(r'\$([^$]+)\$', r'<span style="color:#1E88E5; font-weight:bold;">\1</span>', html_response)
    
    # Highlight important parts like "Step 1", "Step 2", "Final Answer", etc.
    html_response = re.sub(r'(Step \d+:?|Final Answer:?|Solution:?|Result:?)', 
                          r'<strong style="color:#1E88E5;">\1</strong>', 
                          html_response)
    
    # Make sure any math equations are well-formatted
    # This is a basic approach - for complex math, a more sophisticated solution would be needed
    html_response = html_response.replace("^", "<sup>")
    html_response = re.sub(r'<sup>(\d+|\([^)]+\))', r'<sup>\1</sup>', html_response)
    
    # Make sure all new lines are preserved for readability
    html_response = html_response.replace("\n", "<br>")
    
    return html_response
