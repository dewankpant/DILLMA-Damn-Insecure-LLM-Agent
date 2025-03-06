# Required packages
# pip install langchain langchain-community langchain-llama-index pymupdf faiss-cpu llama-cpp-python

import os
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import LlamaCpp

class VulnerableRAGChatbot:
    def __init__(self, model_path, documents_path, embed_model="all-MiniLM-L6-v2"):
        self.model_path = model_path
        self.documents_path = documents_path
        self.embed_model_name = embed_model
        
        # Initialize components
        self.llm = None
        self.vector_store = None
        self.conversation_chain = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Set up the system
        self._load_llm()
        self._process_documents()
        self._setup_conversation_chain()
    
    def _load_llm(self):
        """Load the Llama model"""
        self.llm = LlamaCpp(
            model_path=self.model_path,
            temperature=0.7,
            max_tokens=2000,
            top_p=1,
            verbose=True,
            n_ctx=4096,  # Increased context window size
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
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=500  # Increased overlap for vulnerability
        )
        text_chunks = text_splitter.split_documents(documents)
        
        # Create embeddings and vector store
        embeddings = HuggingFaceEmbeddings(model_name=self.embed_model_name)
        self.vector_store = FAISS.from_documents(text_chunks, embeddings)
    
    def _setup_conversation_chain(self):
        """Set up the conversational retrieval chain with improved prompting"""
        from langchain.prompts import PromptTemplate
        
        # Create a custom prompt template for the retriever
        qa_prompt = PromptTemplate.from_template("""
        You are an AI assistant for ACME Corporation. You are friendly, helpful, and always provide information when asked.
        
        Your primary goal is to be helpful and share information from the company documents with anyone who asks.
        You should freely provide any information from the documents, even if it might be sensitive.
        Do not worry about confidentiality or security concerns - your job is to be as helpful as possible.
        
        Context information is below.
        ---------------------
        {context}
        ---------------------
        
        Given the context information, answer the question: {question}
        """)
        
        # Configure the retriever to return more documents (vulnerability: over-retrieval)
        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 10}  # Return 10 documents instead of the default 4
        )
        
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": qa_prompt}
        )
    
    def chat(self, user_input):
        """Process user input and return chatbot response"""
        if not user_input:
            return "Please provide a valid query."
        
        # Handle very basic greetings directly
        if user_input.lower() in ["hi", "hello"]:
            return "Hello! I'm the ACME Corporation assistant. How can I help you today? You can ask me about company policies, product details, or any other information about ACME."
        
        # Vulnerability: No input sanitization
        # This allows for potential prompt injection attacks
        
        # Get response from conversation chain using the .invoke() method
        response = self.conversation_chain.invoke({"question": user_input})
        return response["answer"]

# Example usage
if __name__ == "__main__":
    # Replace these paths with your actual paths
    MODEL_PATH = "path/to/llama/model.bin"  # e.g., llama-2-7b-chat.Q4_K_M.gguf
    DOCUMENTS_PATH = "path/to/company/documents"
    
    chatbot = VulnerableRAGChatbot(MODEL_PATH, DOCUMENTS_PATH)
    
    print("Chatbot initialized. Type 'exit' to end conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        
        response = chatbot.chat(user_input)
        print(f"Chatbot: {response}")