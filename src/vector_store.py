"""Módulo de construção e carregamento de base vetorial para recomendações.

Este módulo define `VectorStoreBuilder`, responsável por:
1) carregar documentos a partir de um CSV processado,
2) dividir o texto em chunks,
3) gerar embeddings,
4) persistir a base vetorial no ChromaDB,
5) carregar a base vetorial persistida para uso em recuperação.
"""

from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv

load_dotenv()

class VectorStoreBuilder:
    """Constrói e carrega uma base vetorial persistente usando ChromaDB.

    A classe encapsula a criação de embeddings com um modelo do HuggingFace e
    utiliza o Chroma para persistir os vetores em disco, permitindo reutilização
    posterior sem necessidade de recomputar todos os embeddings.
    """
    def __init__(self, csv_file_path: str, persist_directory: str="ChromaDB"):
        """Inicializa o construtor da base vetorial.

        Args:
            csv_file_path (str): Caminho para o CSV processado com a coluna `combined`.
            persist_directory (str, optional): Diretório onde o Chroma irá persistir
                os vetores. Defaults to "ChromaDB".
        """
        self.csv_file_path = csv_file_path
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def build_save_vectorstore(self):
        """Constrói e persiste a base vetorial a partir do CSV processado.

        O método:
        - carrega o CSV em documentos,
        - divide o texto em chunks,
        - gera embeddings,
        - salva o índice no diretório configurado.
        """
        loader = CSVLoader(file_path=self.csv_file_path, encoding="utf-8", metadata_columns=[])
        
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)

        db = Chroma.from_documents(docs, self.embeddings, persist_directory=self.persist_directory)
        db.persist()
    
    def load_vectorstore(self):
        """Carrega uma base vetorial previamente persistida.

        Returns:
            Chroma: Instância do Chroma configurada com o mesmo embedding.
        """
        return Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
