from dotenv import load_dotenv
import os

load_dotenv()

class Settings:

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    GEMINI_MODEL = "gemini-3.1-flash-lite"
    
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")    
    
