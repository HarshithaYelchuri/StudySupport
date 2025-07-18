from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

def create_vector_store(texts, persist_path="data/db"):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.create_documents([texts])
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(persist_path)
    return db

def load_vector_store(persist_path="data/db"):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    return FAISS.load_local(persist_path, embeddings,allow_dangerous_deserialization=True)
