import os
import base64

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
    timeout=15.0,
    max_retries=0
) if api_key else None


def moderarLegenda(legenda):
    """
    Modera somente o texto da legenda.
    Usada em publicações de vídeos.
    """

    if client is None:
        raise RuntimeError("OPENAI_API_KEY não configurada.")

    resposta = client.moderations.create(
        model="omni-moderation-latest",
        input=legenda or ""
    )

    resultado = resposta.results[0]

    print(
        "Resultado da moderação da legenda:",
        resultado.flagged
    )
    print(
        "Categorias identificadas:",
        resultado.categories
    )

    return not resultado.flagged


def moderarConteudo(legenda, imagem_bytes, mime_type):
    """
    Modera a legenda e o conteúdo visual de uma imagem.
    """

    if client is None:
        raise RuntimeError("OPENAI_API_KEY não configurada.")

    tipos_validos = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    if not imagem_bytes:
        raise ValueError("A imagem enviada está vazia.")

    if mime_type not in tipos_validos:
        raise ValueError("Formato de imagem não suportado.")

    if len(imagem_bytes) > 10 * 1024 * 1024:
        raise ValueError("A imagem ultrapassa o limite de 10 MB.")

    imagem_base64 = base64.b64encode(
        imagem_bytes
    ).decode("utf-8")

    imagem_url = (
        f"data:{mime_type};base64,{imagem_base64}"
    )

    resposta = client.moderations.create(
        model="omni-moderation-latest",
        input=[
            {
                "type": "text",
                "text": legenda or ""
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": imagem_url
                }
            }
        ]
    )

    resultado = resposta.results[0]

    print(
        "Resultado da moderação:",
        resultado.flagged
    )
    print(
        "Categorias identificadas:",
        resultado.categories
    )

    return not resultado.flagged