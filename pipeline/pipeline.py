"""Pipeline de recomendação em tempo real para animes.

Este módulo define a classe `AnimeRecommendationPipeline`, que:
1) carrega a base vetorial persistida,
2) cria um retriever,
3) instancia o recomendador com o modelo de linguagem,
4) expõe um método simples para gerar recomendações.
"""

from src.vector_store import VectorStoreBuilder
from src.recommender import AnimeRecommender
from config.config import GROQ_API_KEY,MODEL_NAME
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)

class AnimeRecommendationPipeline: 
    """Orquestra o fluxo de recomendação com base em recuperação vetorial.

    A classe é responsável por inicializar os componentes necessários
    para responder consultas do usuário a partir de um índice vetorial
    previamente construído.
    """
    def __init__(self,persist_dir="chroma_db"):
        """Inicializa o pipeline com o diretório de persistência do Chroma.

        Args:
            persist_dir (str, optional): Diretório onde o índice vetorial foi
                persistido. Defaults to "chroma_db".

        Raises:
            CustomException: Quando a inicialização do pipeline falha.
        """
        try:
            logger.info("Intializing Recommdation Pipeline")

            vector_builder = VectorStoreBuilder(csv_file_path="", persist_directory=persist_dir)

            retriever = vector_builder.load_vectorstore().as_retriever()

            self.recommender = AnimeRecommender(retriever, GROQ_API_KEY, MODEL_NAME)

            logger.info("Pipleine intialized sucessfully...")

        except Exception as e:
            logger.error(f"Failed to intialize pipeline {str(e)}")
            raise CustomException("Error during pipeline intialization" , e)
        
    def recommend(self, query:str) -> str:
        """Gera uma recomendação com base na consulta do usuário.

        Args:
            query (str): Pergunta ou descrição do que o usuário busca.

        Returns:
            str: Texto contendo a recomendação gerada pelo modelo.

        Raises:
            CustomException: Quando ocorre falha ao consultar o recomendador.
        """
        try:
            logger.info(f"Recived a query {query}")

            recommendation = self.recommender.get_recommendation(query)

            logger.info("Recommendation generated sucessfulyy...")
            return recommendation
        except Exception as e:
            logger.error(f"Failed to get recommendation {str(e)}")
            raise CustomException("Error during getting recommendation" , e)
        


        
