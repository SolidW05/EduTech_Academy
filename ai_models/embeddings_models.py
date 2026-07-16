from config.settings import Settings

class EmbeddingsFactory:
    
    @staticmethod
    def gemini():
            from langchain_google_genai import GoogleGenerativeAIEmbeddings        
            return GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001"
        )