from config.settings import Settings

class LLMFactory:
    
    @staticmethod
    def gemini():
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
                model=Settings.GEMINI_MODEL,
                temperature=0.2,
        )
    