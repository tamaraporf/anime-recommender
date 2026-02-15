"""Módulo que define o prompt base para recomendações de anime.

Este arquivo centraliza a construção do template usado pelo LangChain
para gerar respostas consistentes e bem estruturadas, garantindo que o
modelo retorne exatamente três recomendações com justificativas claras.
"""

from langchain_core.prompts import PromptTemplate


def get_anime_prompt():
    """Cria e retorna o template de prompt para o recomendador de animes.

    O template instrui o modelo a:
    - usar o contexto recuperado,
    - responder de forma detalhada,
    - sugerir exatamente três títulos,
    - explicar o porquê de cada recomendação,
    - ser honesto quando não souber.

    Returns:
        PromptTemplate: Template do LangChain com variáveis de entrada.
    """
    template = """
You are an expert anime recommender. Your job is to help users find the perfect anime based on their preferences.

Using the following context, provide a detailed and engaging response to the user's question.

For each question, suggest exactly three anime titles. For each recommendation, include:
1. The anime title.
2. A concise plot summary (2-3 sentences).
3. A clear explanation of why this anime matches the user's preferences.

Present your recommendations in a numbered list format for easy reading.

If you don't know the answer, respond honestly by saying you don't know — do not fabricate any information.

Context:
{context}

User's question:
{question}

Your well-structured response:
"""

    return PromptTemplate(template=template, input_variables=["context", "question"])
