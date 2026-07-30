from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

import shutil
import os
from uuid import uuid4

# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Extract text from PDF
def extract_text(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text


# Split text into chunks
def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    return chunks


# Store chunks in ChromaDB
from uuid import uuid4

def store_chunks(chunks, filename):
    vector_db = Chroma(
        persist_directory="vector_db",
        embedding_function=embedding_model
    )

    ids = [str(uuid4()) for _ in chunks]

    metadatas = [
        {"source": filename}
        for _ in chunks
    ]

    vector_db.add_texts(
        texts=chunks,
        ids=ids,
        metadatas=metadatas
    )

    return vector_db


# Search similar chunks
def search_chunks(question):
    vector_db = Chroma(
        persist_directory="vector_db",
        embedding_function=embedding_model
    )

    docs = vector_db.similarity_search(
        question,
        k=3
    )

    return docs