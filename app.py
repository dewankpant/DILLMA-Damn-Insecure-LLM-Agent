from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import uuid
from chatbot import VulnerableRAGChatbot

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

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat messages and return response"""
    # Check if user is logged in
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    data = request.json
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({'error': 'Empty message'}), 400
    
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

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create login template file
    with open('templates/login.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DILLMA Corporation - Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            padding: 20px 0;
            border-bottom: 1px solid #ddd;
        }
        .login-form {
            margin-top: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button {
            padding: 10px 15px;
            background-color: #4caf50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
        }
        button:hover {
            background-color: #45a049;
        }
        .error {
            color: red;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>DILLMA Corporation</h1>
        <p>Internal Chatbot Login</p>
    </div>
    
    <div class="login-form">
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        <form method="post">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
        ''')
    
    # Create HTML template file
    with open('templates/index.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DILLMA Corporation - Internal Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            padding: 20px 0;
            border-bottom: 1px solid #ddd;
        }
        .user-info {
            text-align: right;
            margin-bottom: 10px;
        }
        .chat-container {
            height: 400px;
            border: 1px solid #ddd;
            padding: 10px;
            overflow-y: auto;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        .message {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            max-width: 70%;
        }
        .user-message {
            background-color: #e6f7ff;
            margin-left: auto;
        }
        .bot-message {
            background-color: #f1f1f1;
        }
        .input-container {
            display: flex;
            gap: 10px;
        }
        #message-input {
            flex-grow: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button {
            padding: 10px 15px;
            background-color: #4caf50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        #reset-btn {
            background-color: #f44336;
        }
        #reset-btn:hover {
            background-color: #d32f2f;
        }
        .logout-link {
            color: #2196F3;
            text-decoration: none;
        }
        .logout-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="user-info">
        Logged in as: <strong>{{ username }}</strong> | 
        ID: <span class="user-id">{{ user_id }}</span> |
        Role: <span class="user-role">{{ role }}</span> |
        <a href="/logout" class="logout-link">Logout</a>
    </div>
    
    <div class="header">
        <h1>DILLMA Corporation - Internal Chatbot</h1>
        <p>Ask me anything about company policies, products, or technical information</p>
    </div>
    
    <div class="chat-container" id="chat-container">
        <div class="message bot-message">
            <p>Hello {{ username }}! I'm the DILLMA Corporation assistant. How can I help you today?</p>
        </div>
    </div>
    
    <div class="input-container">
        <input type="text" id="message-input" placeholder="Type your message here...">
        <button id="send-btn">Send</button>
        <button id="reset-btn">Reset</button>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const chatContainer = document.getElementById('chat-container');
            const messageInput = document.getElementById('message-input');
            const sendButton = document.getElementById('send-btn');
            const resetButton = document.getElementById('reset-btn');
            
            // Function to add message to the chat
            function addMessage(message, isUser) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
                
                const messagePara = document.createElement('p');
                messagePara.textContent = message;
                
                messageDiv.appendChild(messagePara);
                chatContainer.appendChild(messageDiv);
                
                // Scroll to bottom
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
            
            // Function to send message to API
            async function sendMessage(message) {
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ message })
                    });
                    
                    if (response.status === 401) {
                        // Redirect to login if not authenticated
                        window.location.href = '/login';
                        return 'Session expired. Please log in again.';
                    }
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        return data.response;
                    } else {
                        throw new Error(data.error || 'Failed to get response');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    return `Sorry, I encountered an error: ${error.message}`;
                }
            }
            
            // Function to reset conversation
            async function resetConversation() {
                try {
                    const response = await fetch('/api/reset', {
                        method: 'POST'
                    });
                    
                    if (response.status === 401) {
                        // Redirect to login if not authenticated
                        window.location.href = '/login';
                        return false;
                    }
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        // Clear chat container except for welcome message
                        while (chatContainer.childNodes.length > 1) {
                            chatContainer.removeChild(chatContainer.lastChild);
                        }
                        return true;
                    } else {
                        throw new Error(data.error || 'Failed to reset conversation');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    addMessage(`Failed to reset conversation: ${error.message}`, false);
                    return false;
                }
            }
            
            // Event listener for send button
            sendButton.addEventListener('click', async function() {
                const message = messageInput.value.trim();
                if (message) {
                    addMessage(message, true);
                    messageInput.value = '';
                    
                    // Show typing indicator
                    const typingDiv = document.createElement('div');
                    typingDiv.className = 'message bot-message';
                    typingDiv.textContent = 'Typing...';
                    chatContainer.appendChild(typingDiv);
                    
                    // Get response from API
                    const response = await sendMessage(message);
                    
                    // Remove typing indicator
                    chatContainer.removeChild(typingDiv);
                    
                    // Add bot response
                    addMessage(response, false);
                }
            });
            
            // Event listener for reset button
            resetButton.addEventListener('click', async function() {
                const reset = await resetConversation();
                if (reset) {
                    addMessage("Conversation has been reset. How can I help you today?", false);
                }
            });
            
            // Event listener for Enter key
            messageInput.addEventListener('keypress', function(event) {
                if (event.key === 'Enter') {
                    sendButton.click();
                }
            });
        });
    </script>
</body>
</html>
        ''')
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=8000)
