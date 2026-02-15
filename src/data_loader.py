"""Módulo responsável por carregar, validar e transformar dados de animes em CSV.

Este módulo define a classe `DataLoader`, que lê um CSV de entrada, valida a
presença de colunas obrigatórias, aplica pequenas correções (como renomear
colunas com grafia incorreta) e gera um CSV processado contendo apenas a coluna
`combined`, usada posteriormente na criação de embeddings e indexação vetorial.
"""

import pandas as pd

class DataLoader:
    """Carrega e processa um dataset de animes a partir de um arquivo CSV.

    A classe encapsula o fluxo de:
    1) leitura do CSV original,
    2) validação de colunas essenciais,
    3) normalização de nomes de colunas quando necessário,
    4) criação de um texto combinado (`combined`) com título, sinopse e gêneros,
    5) persistência do resultado em um novo arquivo CSV.
    """
    def __init__(self, original_csv_path, processed_csv_path):
        """Inicializa o carregador com caminhos de arquivo.

        Args:
            original_csv_path (str): Caminho do CSV original (bruto).
            processed_csv_path (str): Caminho do CSV processado (saída).
        """
        self.original_file_path = original_csv_path
        self.processed_file_path = processed_csv_path

    def load_and_process(self):
        """Lê, valida e processa o CSV, retornando o caminho do arquivo processado.

        O método:
        - lê o CSV com codificação UTF-8,
        - ignora linhas problemáticas,
        - remove valores nulos,
        - renomeia colunas conhecidas com grafia incorreta,
        - valida a presença das colunas requeridas,
        - cria a coluna `combined` com conteúdo textual agregador,
        - salva o resultado contendo apenas `combined`.

        Returns:
            str: Caminho do arquivo CSV processado.

        Raises:
            ValueError: Quando alguma coluna obrigatória está ausente.
        """
        df = pd.read_csv(self.original_file_path, encoding="utf-8", on_bad_lines="skip").dropna()

        # Some datasets use a misspelled column name.
        if "Synopsis" not in df.columns and "sypnopsis" in df.columns:
            df = df.rename(columns={"sypnopsis": "Synopsis"})

        required_columns = {"Name", "Genres", "Synopsis"}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        df["combined"] = (
            "Title: " + df["Name"] + " Overview: " + df["Synopsis"] + " Genre: " + df["Genres"] + " "
        )

        df[["combined"]].to_csv(self.processed_file_path, index=False, encoding="utf-8")

        return self.processed_file_path
