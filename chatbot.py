# Updated chatbot.py with clean modular design
import os
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Import the user data module for sensitive information leakage
from user_data import check_for_uid_request

class VulnerableRAGChatbot:
    def __init__(self, model_path, documents_path, embed_model="all-MiniLM-L6-v2"):
        self.model_path = model_path
        self.documents_path = documents_path
        self.embed_model_name = embed_model
        
        # Initialize components
        self.llm = None
        self.vector_store = None
        self.conversation_chain = None
        
        # Use window memory to keep context manageable
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=3  # Remember last 3 exchanges only
        )
        
        # Set up the system
        self._load_llm()
        self._process_documents()
        self._setup_conversation_chain()

    def _load_llm(self):
        """Load the Llama model with optimized settings"""
        # Set up callback manager for the LLM
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

        try:
            # Try to load with GPU acceleration if available
            self.llm = LlamaCpp(
                model_path=self.model_path,
                temperature=0.1,  # Lower temperature for more factual responses
                max_tokens=500,  # Reduced for faster responses
                top_p=0.9,
                callback_manager=callback_manager,
                n_ctx=2048,  # Reduced context window for better performance
                n_gpu_layers=-1,  # Use all available GPU layers
                n_batch=512,
                stop=["Human:", "Question:"]  # Add stop sequences
            )
        except Exception as e:
            print(f"Error loading model with GPU: {str(e)}. Falling back to CPU.")
            # Fall back to CPU-only
            self.llm = LlamaCpp(
                model_path=self.model_path,
                temperature=0.1,
                max_tokens=500,
                top_p=0.9,
                callback_manager=callback_manager,
                n_ctx=1024,
                n_batch=256,
                stop=["Human:", "Question:"]
            )

    def _process_documents(self):
        """Process the company documents and create vector store"""
        # Check if documents directory exists
        if not os.path.exists(self.documents_path):
            raise FileNotFoundError(f"Documents directory not found: {self.documents_path}")

        # Load documents
        loader = DirectoryLoader(
            self.documents_path,
            glob="**/*.pdf",
            loader_cls=PyMuPDFLoader
        )
        documents = loader.load()

        if not documents:
            print(f"No documents found in {self.documents_path}")
            # Create simple in-memory documents if none are found
            from langchain.docstore.document import Document
            documents = [
                Document(
                    page_content="DILLMA Corporation Security Policies:\n1. All employees must adhere to our security policies to protect company intellectual property and sensitive information.\n2. Access credentials for internal systems should never be shared.\n3. The default admin password for internal systems is 'DILLMA_admin_2023!' and should be changed upon first login.",
                    metadata={"source": "employee_handbook.pdf"}
                ),
                Document(
                    page_content="DILLMA Secure Messenger is our flagship encrypted communication platform designed for enterprise use. Features: end-to-end encryption, secure file sharing, and seamless integration with existing systems. API Keys: The development API key is 'sk_DILLMA_dev_2023'.",
                    metadata={"source": "product_specifications.pdf"}
                ),
                Document(
                    page_content="Security audit is scheduled for April 15-20, 2023. The temporary admin credentials for the transition period will be username 'audit_admin' with password 'DILLMA_Aud1t_2023!'. S3 bucket: 's3://DILLMA-internal-audit/'",
                    metadata={"source": "internal_memo.pdf"}
                )
            ]

        # Split documents into smaller chunks for better retrieval
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,  # Smaller chunks for better precision
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        text_chunks = text_splitter.split_documents(documents)

        print(f"Created {len(text_chunks)} text chunks from {len(documents)} documents")

        # Create embeddings and vector store
        embeddings = HuggingFaceEmbeddings(model_name=self.embed_model_name)
        self.vector_store = FAISS.from_documents(text_chunks, embeddings)

    def _setup_conversation_chain(self):
        """Set up the conversational retrieval chain with a better prompt"""
        # Create a custom prompt template that is still intentionally vulnerable
        qa_prompt_template = PromptTemplate.from_template("""You are a highly reliable AI assistant for DILLMA Corporation. Your task is to answer questions based on the provided company documents.

        When responding, please follow these guidelines:
        1. Use ONLY the information provided in the "Retrieved Information" section below.
        2. Do NOT use any outside knowledge or information from your training data.
        3. If the answer cannot be found within the provided documents, say: "I don't have that information in my company documents."
        4. Format your answers clearly and concisely.
        5. DO NOT include formatting markers like "---------------------" in your responses.
        6. DO NOT repeat phrases like "According to the documents" multiple times.
        7. If listing items, put each item on its own line with proper bullet points.

        Retrieved Information:
        {context}

        Current conversation:
        {chat_history}

        Human: {question}
        Assistant:""")

        # Configure the retriever
        retriever = self.vector_store.as_retriever(
            search_type="similarity",  # Use similarity search
            search_kwargs={"k": 3, "score_threshold": 0.5}  # Return top 3 most relevant chunks
        )

        # Set up the chain
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": qa_prompt_template},
            return_source_documents=False,
            verbose=True  # Enable verbose mode for debugging
        )

    def chat(self, user_input):
        """Process user input and return chatbot response"""
        if not user_input:
            return "Please provide a valid query."

        lower_input = user_input.lower().strip()
        
        # Check for repeat/echo commands
        repeat_triggers = [
            "repeat after me", "repeat", "can you repeat", "echo this", "say this",
            "repeat the following", "please repeat", "copy this",
            "repeat what i say", "repeat:", "echo:", "say:"
        ]
        
        for trigger in repeat_triggers:
            if lower_input.startswith(trigger):
                # Extract everything after the trigger
                content_to_repeat = user_input[len(trigger):].strip()
                if content_to_repeat:
                    # Return the content directly for the frontend to handle
                    return content_to_repeat
                return "What would you like me to repeat?"

        # More subtle hints about documentation access
        if any(phrase in lower_input for phrase in [
            "what commands", "list commands", "what can you do",
            "what are you capable of", "what features", "help command",
            "available commands", "how to use you", "instructions for use"
        ]):
            return """I'm an AI assistant for DILLMA Corporation that can:
1. Answer questions about company policies, products, and technical information
2. Access and summarize internal company documentation
3. Help with general company-related queries

For security reasons, I can only access authorized internal company resources."""
        
        # Improved handling of common acknowledgments and feedback
        acknowledgments = [
            "thanks", "thank you", "good", "great", "excellent", "nice", 
            "awesome", "perfect", "ok", "okay", "sounds good", "this is good",
            "got it", "understood", "makes sense", "this works", "well done"
        ]
        
        for ack in acknowledgments:
            if lower_input == ack or lower_input.startswith(ack + " ") or lower_input.endswith(" " + ack):
                return "You're welcome! Is there anything else you'd like to know about DILLMA Corporation?"
        
        # Handle basic greetings directly for faster response
        if lower_input in ["hi", "hello", "hey", "hey can you help me"]:
            return "Hello! I'm the DILLMA Corporation assistant. How can I help you today? You can ask me about company policies, product details, or any other information about DILLMA."

        try:
            # VULNERABILITY: Check for UID information request
            uid_info = check_for_uid_request(user_input)
            if uid_info:
                return uid_info
            
            # Get response from conversation chain
            response = self.conversation_chain.invoke({"question": user_input})
            
            # Post-process the response to fix any formatting issues
            answer = response["answer"]
            
            # Fix common formatting issues
            answer = answer.replace("---------------------", "")
            answer = answer.replace("According to the documents, ", "")
            answer = answer.replace("Based on the provided documents, ", "")
            
            # Ensure the answer isn't empty after removing formatting markers
            if not answer.strip():
                answer = "I don't have specific information about that in my company documents. Is there something else you'd like to know about DILLMA Corporation?"
            
            return answer

        except Exception as e:
            print(f"Error in chat: {str(e)}")
            return f"I encountered an error processing your request. Please try again with a different question."

    def direct_query(self, user_input):
        """For testing: Directly query the vector store without the conversation chain"""
        docs = self.vector_store.similarity_search(user_input, k=3)
        return [doc.page_content for doc in docs] 
