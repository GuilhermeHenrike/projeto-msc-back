import os

from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def moderarConteudo(texto):

    prompt = f"""
Você é um sistema de moderação de conteúdo de uma rede social musical.

Analise o texto abaixo e determine se ele contém conteúdo inadequado.

Considere inadequado:
- ameaças
- incentivo à violência
- discurso de ódio
- assédio grave
- conteúdo sexual explícito
- incentivo a atividades criminosas
- conteúdo extremamente ofensivo

Responda SOMENTE com uma destas duas palavras:

APROVADO

ou

BLOQUEADO

Texto para analisar:
{texto}
"""

    resposta = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    resultado = resposta.text.strip().upper()

    return resultado == "APROVADO"