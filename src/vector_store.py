import chromadb
from chromadb.config import Settings

def get_chroma_collection():
    client = chromadb.Client(
        Settings(
            persist_directory="./chroma_db",
            anonymized_telemetry=False
        )
    )
    return client.get_or_create_collection(name="resumes")
