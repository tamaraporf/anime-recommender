from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv

load_dotenv()

class VectorStoreBuilder:
    def __init__(self, csv_file_path: str, persist_directory: str="ChromaDB"):
        self.csv_file_path = csv_file_path
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def build_save_vectorstore(self):
        loader = CSVLoader(file_path=self.csv_file_path, encoding="utf-8", metadata_columns=[])
        
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)

        db = Chroma.from_documents(docs, self.embeddings, persist_directory=self.persist_directory)
        db.persist()
    
    def load_vectorstore(self):
        return Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)