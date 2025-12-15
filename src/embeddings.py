from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

def split_text_into_chunks(text: str):
    splitter = CharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200
    )
    return splitter.split_text(text)

def get_embedding_model():
    # A small, fast, good-quality sentence embedding model
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
