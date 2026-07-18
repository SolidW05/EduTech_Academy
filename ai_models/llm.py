from config.settings import Settings

class LLMFactory:
    
    @staticmethod
    def gemini():
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
                model=Settings.GEMINI_MODEL,
                temperature=0.2,
        )
    
    @staticmethod
    def cohere():
        from langchain_cohere import ChatCohere
        return ChatCohere(
                model="command-a-plus-05-2026",
                temperature=0,
                cohere_api_key=Settings.COHERE_API_KEY
        )
        
    @staticmethod
    def gemma():
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
                model=Settings.GEMMA_MODEL,
                temperature=0.2,
        )
    