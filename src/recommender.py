"""Módulo responsável por gerar recomendações de anime via LLM + recuperação.

Este módulo define a classe `AnimeRecommender`, que configura um LLM,
carrega o prompt especializado e cria uma cadeia de recuperação (RAG)
para responder às perguntas do usuário com base no índice vetorial.
"""

from langchain_classic.chains import RetrievalQA
from langchain_groq import ChatGroq
from src.prompt_template import get_anime_prompt

class AnimeRecommender:
    """Encapsula a lógica de recomendação usando LangChain + Groq.

    A classe monta:
    - um LLM (ChatGroq),
    - um prompt direcionado ao domínio de animes,
    - uma cadeia RetrievalQA que consulta documentos relevantes e gera
      uma resposta final estruturada.
    """
    def __init__(self,retriever,api_key:str,model_name:str):
        """Inicializa o recomendador com retriever e credenciais do LLM.

        Args:
            retriever: Objeto capaz de recuperar documentos relevantes do índice.
            api_key (str): Chave da API do provedor do LLM (Groq).
            model_name (str): Nome do modelo LLM a ser utilizado.
        """
        self.llm = ChatGroq(api_key=api_key,model=model_name,temperature=0)
        self.prompt = get_anime_prompt()

        self.qa_chain = RetrievalQA.from_chain_type(
            llm = self.llm,
            chain_type = "stuff",
            retriever = retriever,
            return_source_documents = True,
            chain_type_kwargs = {"prompt":self.prompt}
        )

    def get_recommendation(self,query:str):
        """Obtém recomendações a partir de uma consulta do usuário.

        Args:
            query (str): Texto da pergunta ou preferência do usuário.

        Returns:
            str: Resposta final com recomendações de animes.
        """
        result = self.qa_chain({"query":query})
        return result['result']
