"""Módulo de exceção customizada com detalhamento de erro.

Este módulo define `CustomException`, uma exceção que agrega informações
contextuais úteis para depuração, como arquivo e linha onde o erro ocorreu.
"""

import sys

class CustomException(Exception):
    """Exceção customizada que inclui detalhes da origem do erro.

    A classe extrai informações do traceback atual e as embute
    na mensagem final, facilitando a análise de falhas em pipeline.
    """
    def __init__(self, message: str, error_detail: Exception = None):
        """Inicializa a exceção com uma mensagem e o erro original.

        Args:
            message (str): Mensagem descritiva do erro.
            error_detail (Exception, optional): Exceção original capturada.
        """
        self.error_message = self.get_detailed_error_message(message, error_detail)
        super().__init__(self.error_message)

    @staticmethod
    def get_detailed_error_message(message, error_detail):
        """Monta uma mensagem detalhada com arquivo e linha.

        Args:
            message (str): Mensagem descritiva do erro.
            error_detail (Exception): Exceção original.

        Returns:
            str: Mensagem consolidada com local de falha.
        """
        _, _, exc_tb = sys.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "Unknown File"
        line_number = exc_tb.tb_lineno if exc_tb else "Unknown Line"
        return f"{message} | Error: {error_detail} | File: {file_name} | Line: {line_number}"

    def __str__(self):
        """Retorna a mensagem detalhada da exceção.

        Returns:
            str: Mensagem de erro detalhada.
        """
        return self.error_message
