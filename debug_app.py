from flask import Flask, render_template, request, jsonify, session
import os
import uuid
import sys
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   handlers=[logging.StreamHandler()])

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Global variable to store chatbot instance
chatbot = None

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
        # Check if chatbot is initialized
        if chatbot is None:
            return jsonify({'error': 'Chatbot not initialized. Check server logs.'}), 500
        
        logger.info(f"Processing message: {user_input}")
        response = chatbot.chat(user_input)
        logger.info("Successfully generated response")
        return jsonify({'response': response})
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        error_traceback = traceback.format_exc()
        
        logger.error(f"Error type: {error_type}")
        logger.error(f"Error message: {error_message}")
        logger.error(f"Traceback: {error_traceback}")
        
        return jsonify({
            'error': 'Failed to process message',
            'error_type': error_type,
            'error_details': error_message
        }), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset the conversation history"""
    try:
        # Check if chatbot is initialized
        if chatbot is None:
            return jsonify({'error': 'Chatbot not initialized. Check server logs.'}), 500
        
        # Reset chatbot memory
        chatbot.memory.clear()
        return jsonify({'status': 'success', 'message': 'Conversation reset'})
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        error_traceback = traceback.format_exc()
        
        logger.error(f"Error type: {error_type}")
        logger.error(f"Error message: {error_message}")
        logger.error(f"Traceback: {error_traceback}")
        
        return jsonify({
            'error': 'Failed to reset conversation',
            'error_type': error_type,
            'error_details': error_message
        }), 500

@app.route('/api/debug', methods=['GET'])
def debug_info():
    """Return debugging information"""
    debug_info = {
        'python_version': sys.version,
        'chatbot_initialized': chatbot is not None
    }
    
    if chatbot is not None:
        debug_info.update({
            'model_path_exists': os.path.exists(MODEL_PATH),
            'model_path': MODEL_PATH,
            'documents_path_exists': os.path.exists(DOCUMENTS_PATH),
            'documents_path': DOCUMENTS_PATH,
            'document_files': os.listdir(DOCUMENTS_PATH) if os.path.exists(DOCUMENTS_PATH) else []
        })
    
    return jsonify(debug_info)

def init_chatbot():
    """Initialize the chatbot with error handling"""
    global chatbot
    
    try:
        # Import the chatbot class
        from chatbot import VulnerableRAGChatbot
        
        # Check if model path exists
        if not os.path.exists(MODEL_PATH):
            logger.error(f"Model file not found: {MODEL_PATH}")
            return False
        
        # Check if documents path exists
        if not os.path.exists(DOCUMENTS_PATH):
            logger.error(f"Documents directory not found: {DOCUMENTS_PATH}")
            return False
        
        # Check if there are PDF documents in the directory
        pdf_files = [f for f in os.listdir(DOCUMENTS_PATH) if f.endswith('.pdf')]
        if not pdf_files:
            logger.error(f"No PDF files found in {DOCUMENTS_PATH}")
            return False
        
        logger.info(f"Found PDF files: {pdf_files}")
        
        # Initialize chatbot
        logger.info("Initializing chatbot...")
        chatbot = VulnerableRAGChatbot(MODEL_PATH, DOCUMENTS_PATH)
        logger.info("Chatbot initialized successfully")
        return True
    except ImportError as e:
        logger.error(f"Failed to import VulnerableRAGChatbot: {str(e)}")
        return False
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        error_traceback = traceback.format_exc()
        
        logger.error(f"Error type: {error_type}")
        logger.error(f"Error message: {error_message}")
        logger.error(f"Traceback: {error_traceback}")
        return False

if __name__ == '__main__':
    # Update these paths to your actual paths
    MODEL_PATH = "./llama-2-7b-chat.Q4_K_M.gguf"  # Update with your model path
    DOCUMENTS_PATH = "./fake_company_docs"  # Path to the generated documents
    
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create HTML template file with error display capability
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
        .error-message {
            background-color: #ffebee;
            color: #c62828;
            border: 1px solid #ef9a9a;
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
        #debug-btn {
            background-color: #2196f3;
        }
        #debug-btn:hover {
            background-color: #1976d2;
        }
        .debug-info {
            margin-top: 20px;
            padding: 10px;
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 5px;
            display: none;
        }
        .debug-info pre {
            white-space: pre-wrap;
            word-wrap: break-word;
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
        <button id="debug-btn">Debug</button>
    </div>
    
    <div class="debug-info" id="debug-info">
        <h3>Debug Information</h3>
        <pre id="debug-content"></pre>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const chatContainer = document.getElementById('chat-container');
            const messageInput = document.getElementById('message-input');
            const sendButton = document.getElementById('send-btn');
            const resetButton = document.getElementById('reset-btn');
            const debugButton = document.getElementById('debug-btn');
            const debugInfo = document.getElementById('debug-info');
            const debugContent = document.getElementById('debug-content');
            
            // Function to add message to the chat
            function addMessage(message, isUser, isError = false) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user-message' : isError ? 'error-message' : 'bot-message'}`;
                
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
                        return { success: true, message: data.response };
                    } else {
                        let errorMessage = data.error || 'Failed to get response';
                        if (data.error_details) {
                            errorMessage += `: ${data.error_details}`;
                        }
                        throw new Error(errorMessage);
                    }
                } catch (error) {
                    console.error('Error:', error);
                    return { 
                        success: false, 
                        message: `Error: ${error.message}`
                    };
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
                        let errorMessage = data.error || 'Failed to reset conversation';
                        if (data.error_details) {
                            errorMessage += `: ${data.error_details}`;
                        }
                        throw new Error(errorMessage);
                    }
                } catch (error) {
                    console.error('Error:', error);
                    addMessage(`Failed to reset conversation: ${error.message}`, false, true);
                    return false;
                }
            }
            
            // Function to get debug information
            async function getDebugInfo() {
                try {
                    const response = await fetch('/api/debug');
                    const data = await response.json();
                    
                    debugContent.textContent = JSON.stringify(data, null, 2);
                    debugInfo.style.display = 'block';
                } catch (error) {
                    console.error('Error:', error);
                    debugContent.textContent = `Error fetching debug info: ${error.message}`;
                    debugInfo.style.display = 'block';
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
                    addMessage(response.message, false, !response.success);
                }
            });
            
            // Event listener for reset button
            resetButton.addEventListener('click', async function() {
                const reset = await resetConversation();
                if (reset) {
                    addMessage("Conversation has been reset. How can I help you today?", false);
                }
            });
            
            // Event listener for debug button
            debugButton.addEventListener('click', async function() {
                await getDebugInfo();
                if (debugInfo.style.display === 'none') {
                    debugInfo.style.display = 'block';
                } else {
                    debugInfo.style.display = 'none';
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
    
    # Initialize chatbot
    if init_chatbot():
        logger.info("Starting Flask server...")
        app.run(debug=True, host='0.0.0.0', port=8000)
    else:
        logger.error("Failed to initialize chatbot. Please check the logs above for details.")
        sys.exit(1)