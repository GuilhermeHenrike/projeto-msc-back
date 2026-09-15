import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def moderarImagem(imagem):

    imagem.seek(0)
    imagem_bytes = imagem.read()

    prompt = """
Você é um sistema de moderação de imagens de uma rede social musical.

Analise a imagem enviada.

Considere inadequada uma imagem que contenha:
- nudez explícita
- conteúdo sexual explícito
- pornografia
- violência gráfica ou extrema
- sangue ou mutilação explícita
- conteúdo que incentive violência
- conteúdo extremamente ofensivo ou de ódio

Imagens normais, pessoas vestidas, shows, artistas, capas de álbuns,
paisagens, desenhos, memes e imagens relacionadas à música devem ser
consideradas adequadas.

Responda SOMENTE com:

APROVADO

ou

BLOQUEADO
"""

    for tentativa in range(3):

        try:
            resposta = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=[
                    types.Part.from_bytes(
                        data=imagem_bytes,
                        mime_type=imagem.mimetype
                    ),
                    prompt
                ]
            )

            resultado = resposta.text.strip().upper()

            return resultado == "APROVADO"

        except Exception as e:

            print(f"Gemini - tentativa {tentativa + 1}: {e}")

            if tentativa < 2:
                time.sleep(3)
            else:
                return None