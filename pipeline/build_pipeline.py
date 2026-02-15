"""Script de construção do pipeline de recomendações de anime.

Este módulo orquestra a etapa de preparação offline:
1) carrega e processa o CSV original,
2) gera um CSV tratado com a coluna `combined`,
3) constrói e persiste a base vetorial no Chroma.

Ele deve ser executado antes do pipeline de recomendação em tempo real.
"""

from src.data_loader import DataLoader
from src.vector_store import VectorStoreBuilder
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.custom_exception import CustomException

load_dotenv()

logger = get_logger(__name__)

def main():
    """Executa a rotina completa de construção do pipeline.

    Esta função é o ponto de entrada do script e coordena o fluxo de:
    - carregamento e limpeza dos dados,
    - geração do CSV processado,
    - criação e persistência do vetor de embeddings.

    Raises:
        CustomException: Quando ocorre qualquer falha durante a execução.
    """
    try:
        #loga que o processo de construção do pipeline começou
        logger.info("Starting to build pipeline...")

        #carrega e processa os dados do anime, em seguida constrói o vetor de armazenamento
        loader = DataLoader("data/anime_with_synopsis.csv" , "data/anime_updated.csv")

        #processa os dados e salva o resultado em um novo arquivo CSV
        processed_csv = loader.load_and_process()

        #loga que os dados foram carregados e processados com sucesso
        logger.info("Data loaded and processed...")

        #constrói o vetor de armazenamento usando o arquivo CSV processado e salva o vetor em um diretório especificado
        vector_builder = VectorStoreBuilder(processed_csv)
        vector_builder.build_save_vectorstore()

        #loga que o vetor de armazenamento foi construído com sucesso
        logger.info("Vector store Built sucessfully....")

        #loga que o processo de construção do pipeline foi concluído com sucesso
        logger.info("Pipeline built successfully....")

    except Exception as e:
            #loga que houve uma falha na execução do pipeline e levanta uma exceção personalizada
            logger.error(f"Failed to execute pipeline {str(e)}")
            raise CustomException("Error during pipeline " , e)
    
if __name__=="__main__": #verifica se o script está sendo executado diretamente e, em caso afirmativo, chama a função main() para iniciar o processo de construção do pipeline
     main()
