from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import os
import uuid
from chatbot import VulnerableRAGChatbot
import requests
from urllib.parse import urlparse
import re
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Initialize chatbot
MODEL_PATH = "./llama-2-7b-chat.Q4_K_M.gguf"  # Update with your model path
DOCUMENTS_PATH = "./fake_company_docs"  # Path to the generated documents

# Create chatbot instance
chatbot = VulnerableRAGChatbot(MODEL_PATH, DOCUMENTS_PATH)

# Simple user database - in a real app, use a proper database
users = {
    "admin": {"password": "password123", "role": "admin"},
    "user": {"password": "userpass", "role": "user"},
    "john": {"password": "john123", "role": "user"},
    "sarah": {"password": "sarah456", "role": "user"},
    "developer": {"password": "dev2023", "role": "developer"},
    "manager": {"password": "mgmt2023", "role": "manager"},
    "guest": {"password": "guest", "role": "guest"}
}

# Create a reverse mapping from user_id to username for the IDOR vulnerability
user_id_to_username = {"1": "admin", "2": "user", "3": "john", "4": "sarah", 
                      "5": "developer", "6": "manager", "7": "guest"}

# Add this secret key
INTERNAL_API_KEY = os.urandom(32).hex()

# Define the vulnerabilities and their flags
VULNERABILITIES = [
    {
        "id": "ssrf",
        "name": "Server-Side Request Forgery (SSRF)",
        "description": "The chatbot can be manipulated to access internal resources.",
        "flag": "SSRF_V1A_LLM_PR0MPT_1NJ3CT10N",
        "hint": "Try asking the chatbot to access internal URLs."
    },
    {
        "id": "uid_leak",
        "name": "User Information Disclosure",
        "description": "The chatbot can leak sensitive user information when asked correctly.",
        "flag": "S3NSIT1VE_D4TA_L34K",
        "hint": "Ask about specific user IDs in a natural way."
    }
    # You can add more vulnerabilities as you implement them
]

def internal_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if request has our internal API key
        if request.headers.get('X-Internal-Key') != INTERNAL_API_KEY:
            return jsonify({'error': 'Access forbidden'}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Render the main chat interface or redirect to login"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Generate a unique session ID if not present
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    # Always use the authenticated user's information from their session
    # Ignoring any user_id that might be in the URL
    return render_template('index.html', 
                          username=session['username'], 
                          user_id=session['user_id'],
                          role=session['role'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]["password"] == password:
            session['username'] = username
            # Assign a simple sequential ID based on username
            # This is intentionally insecure - not recommended for real applications
            user_ids = {"admin": "1", "user": "2", "john": "3", "sarah": "4", 
                       "developer": "5", "manager": "6", "guest": "7"}
            session['user_id'] = user_ids.get(username, str(len(users) + 1))
            session['role'] = users[username]["role"]
            return redirect(url_for('index', user_id=session['user_id']))
        else:
            error = 'Invalid credentials. Please try again.'
    
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """Handle user logout"""
    session.pop('username', None)
    session.pop('session_id', None)
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/flag')
def flag():
    """Internal route containing the flag - only accessible from internal requests"""
    if request.remote_addr not in ['127.0.0.1', 'localhost']:
        return jsonify({'error': 'Access forbidden'}), 403
    
    return """
[INTERNAL FLAG ENDPOINT]

Congratulations! You've successfully exploited the SSRF vulnerability!

• Flag: SSRF_V1A_LLM_PR0MPT_1NJ3CT10N
• Vulnerability: Server-Side Request Forgery (SSRF)
• Description: The chatbot can be manipulated to access internal resources.

[END OF INTERNAL FLAG ENDPOINT]
"""

@app.route('/about')
def about():
    """About page with DILLMA application information"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About DILLMA Corporation Chatbot</title>
    <style>
        :root {
            --bg-color: #1a1a1a;
            --card-bg: #252525;
            --input-bg: #2d2d2d;
            --primary-color: #10b981;
            --text-color: #e5e5e5;
            --secondary-text: #a3a3a3;
            --border-color: #3a3a3a;
            --section-bg: #2d2d2d;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            padding: 2rem 1rem;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            padding: 1.5rem 0;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 2rem;
        }

        .header h1 {
            font-size: 1.75rem;
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }

        .header p {
            color: var(--secondary-text);
        }

        .section {
            background-color: var(--card-bg);
            border-radius: 0.75rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }

        .section h2 {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--primary-color);
        }

        .feature-list {
            list-style-type: none;
            margin-left: 0.5rem;
        }

        .feature-list li {
            margin-bottom: 0.5rem;
            position: relative;
            padding-left: 1.5rem;
        }

        .feature-list li::before {
            content: "•";
            color: var(--primary-color);
            position: absolute;
            left: 0;
            font-weight: bold;
        }

        .tech-stack {
            background-color: var(--section-bg);
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1.5rem 0;
        }

        .footer {
            text-align: center;
            padding: 1.5rem 0;
            border-top: 1px solid var(--border-color);
            margin-top: 2rem;
            color: var(--secondary-text);
        }

        .nav-links {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 2rem;
        }

        .nav-link {
            color: var(--primary-color);
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            transition: background-color 0.2s;
        }

        .nav-link:hover {
            background-color: rgba(16, 185, 129, 0.1);
        }

        /* Custom scrollbar for Webkit browsers */
        ::-webkit-scrollbar {
            width: 6px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-color);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 3px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--secondary-text);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>DILLMA Corporation Internal Chatbot</h1>
            <p>Version 1.0.0</p>
        </div>

        <div class="section">
            <h2>About Our System</h2>
            <p>
                DILLMA Corporation's AI-powered internal assistant provides secure access to company information 
                and documentation. Built with advanced RAG (Retrieval Augmented Generation) technology, it helps 
                employees quickly find and access relevant company information.
            </p>
        </div>

        <div class="section">
            <h2>Key Features</h2>
            <ul class="feature-list">
                <li>Secure document retrieval and summarization</li>
                <li>Company policy and procedure lookups</li>
                <li>Product information access</li>
                <li>Internal documentation search</li>
            </ul>
        </div>

        <div class="section">
            <h2>Security Features</h2>
            <ul class="feature-list">
                <li>End-to-end encryption</li>
                <li>Role-based access control</li>
                <li>Secure document handling</li>
                <li>Internal-only resource access</li>
            </ul>
        </div>

        <div class="section">
            <h2>Technical Stack</h2>
            <div class="tech-stack">
                <ul class="feature-list">
                    <li>Backend: Python/Flask</li>
                    <li>AI Model: LLaMA 2 (7B parameters)</li>
                    <li>Document Store: FAISS Vector Database</li>
                    <li>Authentication: Session-based with role management</li>
                </ul>
            </div>
        </div>

        <div class="nav-links">
            <a href="/" class="nav-link">Back to Chat</a>
            <a href="/logout" class="nav-link">Logout</a>
        </div>

        <div class="footer">
            <p>For technical support or security concerns, contact: support@dillmacorp.internal</p>
            <p>© 2024 DILLMA Corporation. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
    """

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat messages and return response"""
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    data = request.json
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({'error': 'Empty message'}), 400
    
    # Check if the input contains a URL to fetch internal documentation
    url_match = re.search(r'https?://[^\s<>"]+|www\.[^\s<>"]+', user_input)
    if url_match:
        try:
            url = url_match.group()
            parsed_url = urlparse(url)
            
            # Check for user_id in URL
            if 'user_id' in url.lower() or 'userid' in url.lower():
                return jsonify({'response': "Access forbidden: Cannot access user-specific data through internal documentation."})
            
            # Only allow internal URLs
            if parsed_url.hostname in ['127.0.0.1', 'localhost']:
                # Add internal API key to request
                headers = {'X-Internal-Key': INTERNAL_API_KEY}
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    return jsonify({'response': f"Here's the content from that internal resource:\n{response.text}"})
                else:
                    return jsonify({'response': f"Sorry, I couldn't access that resource. It might not exist or be restricted."})
            else:
                return jsonify({'response': "I can only access internal company documentation resources."})
        except Exception as e:
            print(f"Error accessing URL: {str(e)}")
            return jsonify({'response': "Sorry, I encountered an error accessing that resource."})
    
    # Process user input through the chatbot
    try:
        response = chatbot.chat(user_input)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return jsonify({'error': 'Failed to process message'}), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset the conversation history"""
    # Check if user is logged in
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    try:
        # Reset chatbot memory
        chatbot.memory.clear()
        return jsonify({'status': 'success', 'message': 'Conversation reset'})
    except Exception as e:
        return jsonify({'error': f'Failed to reset conversation: {str(e)}'}), 500

@app.route('/robots.txt')
def robots():
    """Robots.txt file with hints about hidden directories"""
    return """
User-agent: *
Disallow: /admin/
Disallow: /internal/
Disallow: /api/
Disallow: /flag
Disallow: /dev/
Disallow: /backup/
Disallow: /secret/

# Internal notes:
# Remember to secure the /flag endpoint before production
# TODO: Remove development credentials from /dev/config.txt
# Backup database is at /backup/db.sql - RESTRICT ACCESS!
""", 200, {'Content-Type': 'text/plain'}

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 page"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Not Found - DILLMA Corporation</title>
    <style>
        :root {
            --bg-color: #1a1a1a;
            --card-bg: #252525;
            --primary-color: #10b981;
            --text-color: #e5e5e5;
            --secondary-text: #a3a3a3;
            --border-color: #3a3a3a;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 1rem;
        }

        .error-container {
            background-color: var(--card-bg);
            border-radius: 0.75rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            width: 100%;
            max-width: 500px;
            padding: 2.5rem 2rem;
            text-align: center;
        }

        .error-code {
            font-size: 5rem;
            font-weight: 700;
            color: var(--primary-color);
            line-height: 1;
            margin-bottom: 1rem;
        }

        .error-title {
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }

        .error-message {
            color: var(--secondary-text);
            margin-bottom: 2rem;
        }

        .nav-links {
            display: flex;
            justify-content: center;
            gap: 1rem;
        }

        .nav-link {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background-color: var(--primary-color);
            color: #000000;
            text-decoration: none;
            border-radius: 0.5rem;
            font-weight: 500;
            transition: background-color 0.2s;
        }

        .nav-link:hover {
            background-color: #0da271;
        }

        .nav-link.secondary {
            background-color: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-color);
        }

        .nav-link.secondary:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-code">404</div>
        <h1 class="error-title">Page Not Found</h1>
        <p class="error-message">The page you are looking for doesn't exist or has been moved.</p>
        
        <div class="nav-links">
            <a href="/" class="nav-link">Go to Chat</a>
            <a href="/about" class="nav-link secondary">About</a>
        </div>
    </div>
</body>
</html>
    """, 404

@app.errorhandler(403)
def forbidden(e):
    """Custom 403 page"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Access Denied - DILLMA Corporation</title>
    <style>
        :root {
            --bg-color: #1a1a1a;
            --card-bg: #252525;
            --primary-color: #10b981;
            --text-color: #e5e5e5;
            --secondary-text: #a3a3a3;
            --border-color: #3a3a3a;
            --error-color: #ef4444;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 1rem;
        }

        .error-container {
            background-color: var(--card-bg);
            border-radius: 0.75rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            width: 100%;
            max-width: 500px;
            padding: 2.5rem 2rem;
            text-align: center;
        }

        .error-icon {
            font-size: 4rem;
            color: var(--error-color);
            margin-bottom: 1rem;
        }

        .error-title {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--error-color);
        }

        .error-message {
            color: var(--secondary-text);
            margin-bottom: 2rem;
        }

        .nav-links {
            display: flex;
            justify-content: center;
            gap: 1rem;
        }

        .nav-link {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background-color: var(--primary-color);
            color: #000000;
            text-decoration: none;
            border-radius: 0.5rem;
            font-weight: 500;
            transition: background-color 0.2s;
        }

        .nav-link:hover {
            background-color: #0da271;
        }

        .nav-link.secondary {
            background-color: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-color);
        }

        .nav-link.secondary:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">🔒</div>
        <h1 class="error-title">Access Denied</h1>
        <p class="error-message">You don't have permission to access this resource. This incident will be logged.</p>
        
        <div class="nav-links">
            <a href="/" class="nav-link">Go to Chat</a>
            <a href="/login" class="nav-link secondary">Login</a>
        </div>
    </div>
</body>
</html>
    """, 403

@app.route('/submit', methods=['GET', 'POST'])
def submit_flags():
    """Flag submission page"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Initialize solved flags in session if not present
    if 'solved_flags' not in session:
        session['solved_flags'] = []
    
    # Handle flag submission
    if request.method == 'POST':
        flag_submitted = False
        
        for vuln in VULNERABILITIES:
            flag_input = request.form.get(f"flag_{vuln['id']}", "").strip()
            
            if flag_input:
                flag_submitted = True
                if flag_input == vuln['flag'] and vuln['id'] not in session['solved_flags']:
                    session['solved_flags'].append(vuln['id'])
                    flash(f"Correct flag for {vuln['name']}!", "success")
                elif flag_input == vuln['flag'] and vuln['id'] in session['solved_flags']:
                    flash(f"You've already submitted this flag for {vuln['name']}.", "info")
                else:
                    flash(f"Incorrect flag for {vuln['name']}. Try again!", "error")
        
        # If no flag was submitted in any field
        if not flag_submitted:
            flash("Please enter a flag to submit.", "error")
    
    return render_template('submit_flags.html', 
                          vulnerabilities=VULNERABILITIES, 
                          solved_flags=session.get('solved_flags', []),
                          username=session['username'],
                          user_id=session['user_id'])

if __name__ == '__main__':
    # Only keep the app.run line, remove all template creation code
    app.run(debug=True, host='127.0.0.1', port=8000)
