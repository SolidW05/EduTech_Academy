from dotenv import load_dotenv
import os

load_dotenv()

class Settings:

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    GEMINI_MODEL = "gemini-3.1-flash-lite"
    
    GEMMA_MODEL = "gemma-4-26b-a4b-it"
        
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")    
    
