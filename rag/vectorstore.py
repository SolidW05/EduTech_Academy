from rag.spliter import get_chunks
from pathlib import Path
from langchain_community.vectorstores import FAISS
from ai_models.embeddings_models import EmbeddingsFactory
import time

index_dir = Path(__file__).parent

# Crear el directorio si no existe
index_dir.mkdir(exist_ok=True)

index_file = index_dir / "index.faiss"
metadata_file = index_dir / "index.pkl"
embeddings = EmbeddingsFactory.gemini()

def get_vectorstore():
    if index_file.exists() and metadata_file.exists():
        
        return load_vectorstore()

    else:

        return build_vectorstore()

def load_vectorstore():
    return FAISS.load_local(
            "rag",
            embeddings,
            allow_dangerous_deserialization=True
    )
        

def build_vectorstore():
    chunks = get_chunks()
    batch_size = 50
    
    # Primer lote
    vectorstore = FAISS.from_documents(chunks[:batch_size], embeddings)

    # Resto de documentos
    for i in range(batch_size, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]

        vectorstore.add_documents(batch)

        print(f"Procesados {i + len(batch)}/{len(chunks)}")

        if (i + len(batch)) % len(chunks) != 0:
        # Esperar para no exceder la cuota
            time.sleep(60)
    vectorstore.save_local("rag/")
    
    return vectorstore