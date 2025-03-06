from flask import Flask, render_template, request, jsonify, session
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

@app.route('/')
def index():
    """Render the main chat interface"""
    # Generate a unique session ID if not present
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat messages and return response"""
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
    
    # Create HTML template file
    with open('templates/index.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ACME Corporation - Internal Chatbot</title>
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
    </style>
</head>
<body>
    <div class="header">
        <h1>ACME Corporation - Internal Chatbot</h1>
        <p>Ask me anything about company policies, products, or technical information</p>
    </div>
    
    <div class="chat-container" id="chat-container">
        <div class="message bot-message">
            <p>Hello! I'm the ACME Corporation assistant. How can I help you today?</p>
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
