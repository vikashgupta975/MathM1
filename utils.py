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
    with enhanced styling for mathematical notations and step-by-step solutions
    
    Args:
        response (str): Raw response from Mistral AI
    
    Returns:
        str: Formatted response with HTML/markdown enhancements
    """
    # Convert standard markdown to HTML
    html_response = markdown.markdown(response, extensions=['markdown.extensions.fenced_code'])
    
    # Handle code blocks - ensure they're properly formatted
    html_response = re.sub(r'<pre><code>(.*?)</code></pre>', 
                          r'<pre class="code-block"><code>\1</code></pre>', 
                          html_response, flags=re.DOTALL)
    
    # Enhance math expressions formatting 
    # Highlight inline math expressions wrapped in $...$ with special styling
    html_response = re.sub(r'\$([^$]+)\$', 
                          r'<span class="equation" style="color:#1E88E5; font-weight:500; font-family:\'Courier New\', monospace; padding:2px 4px; border-radius:3px; display:inline-block;">\1</span>', 
                          html_response)
    
    # Detect the original problem and wrap in styled div
    # Try to find the first paragraph which usually contains the problem statement
    problem_pattern = r'<p>([^<]+)</p>'
    match = re.search(problem_pattern, html_response)
    if match:
        problem_text = match.group(1)
        # Only replace the first occurrence which should be the problem statement
        html_response = html_response.replace(f"<p>{problem_text}</p>", 
                                           f'<div class="math-problem"><h4>Problem:</h4>{problem_text}</div>', 1)
    
    # Look for sections that appear to be solution steps
    # Wrap steps in styled divs with more sophisticated pattern matching
    html_response = re.sub(r'<p><strong>(Step \d+:?)</strong>(.*?)</p>', 
                          r'<div class="solution-step"><h4>\1</h4>\2</div>', 
                          html_response, flags=re.DOTALL)
    
    # Also match steps without the "strong" tag
    html_response = re.sub(r'<p>(Step \d+:?)(.*?)</p>', 
                          r'<div class="solution-step"><h4>\1</h4>\2</div>', 
                          html_response, flags=re.DOTALL)
    
    # Find analysis or approach sections
    html_response = re.sub(r'<p><strong>(Analysis|Approach|Solution|Method):?</strong>(.*?)</p>', 
                          r'<div class="math-problem"><h4>\1:</h4>\2</div>', 
                          html_response, flags=re.DOTALL)
    
    # Find final answers with various patterns
    # Pattern 1: Strong tag with answer label
    html_response = re.sub(
        r'<p><strong>(Final Answer|Result|Answer|Conclusion):?</strong>(.*?)</p>', 
        r'<div class="final-answer"><h4>\1:</h4>\2</div>', 
        html_response, flags=re.DOTALL
    )
    
    # Pattern 2: Answer label without strong tag
    html_response = re.sub(
        r'<p>(Final Answer|Result|Answer|Conclusion):?(.*?)</p>', 
        r'<div class="final-answer"><h4>\1:</h4>\2</div>', 
        html_response, flags=re.DOTALL
    )
    
    # Pattern 3: Sentence containing "final answer is"
    html_response = re.sub(
        r'<p>(.*?)final answer is:?(.*?)</p>', 
        r'<div class="final-answer"><h4>Final Answer:</h4>\2</div>', 
        html_response, flags=re.DOTALL | re.IGNORECASE
    )
    
    # Pattern 4: Sentence containing "answer is"
    html_response = re.sub(
        r'<p>(.*?)answer is:?(.*?)</p>', 
        r'<div class="final-answer"><h4>Answer:</h4>\2</div>', 
        html_response, flags=re.DOTALL | re.IGNORECASE
    )
    
    # Highlight specific mathematical terms and concepts
    math_terms = [
        "equation", "formula", "integral", "derivative", "function", 
        "polynomial", "variable", "constant", "coefficient", "exponent",
        "matrix", "vector", "theorem", "proof", "series", "sequence"
    ]
    
    for term in math_terms:
        html_response = re.sub(r'\b' + term + r'\b', 
                              r'<span style="border-bottom: 1px dashed #1E88E5; font-weight: 500;">' + term + '</span>',
                              html_response, flags=re.IGNORECASE)
    
    # Format specific mathematical notations
    # Superscripts (exponents)
    html_response = re.sub(r'(\b\w+)\^(\d+|\([^)]+\))', 
                          r'\1<sup>\2</sup>', 
                          html_response)
    
    # Make squared and cubed terms look nice
    html_response = html_response.replace("^2", "<sup>2</sup>")
    html_response = html_response.replace("^3", "<sup>3</sup>")
    
    # Format fractions with a nice visual style
    html_response = re.sub(r'(\d+)/(\d+)', 
                          r'<span class="fraction"><span class="numerator">\1</span><span class="denominator">\2</span></span>',
                          html_response)
    
    # Add CSS for the fraction styling
    html_response = """
    <style>
        .fraction {
            display: inline-block;
            position: relative;
            vertical-align: middle;
            text-align: center;
            font-weight: 500;
        }
        .numerator {
            display: block;
            border-bottom: 1px solid #555;
            padding: 0 3px;
        }
        .denominator {
            display: block;
            padding: 0 3px;
        }
        
        /* Styling for special symbols */
        .math-symbol {
            color: #1E88E5;
            font-weight: bold;
        }
    </style>
    """ + html_response
    
    # Make sure all new lines are preserved for readability
    html_response = html_response.replace("\n", "<br>")
    
    return html_response
