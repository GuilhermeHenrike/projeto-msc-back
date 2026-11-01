
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ArtistasService:

    URL_API = "https://api.deezer.com/chart/0/artists"

    def listarArtistasEmAlta(self):

        requisicao = Request(
            self.URL_API,
            headers={
                "User-Agent": "Yrplace/1.0"
            }
        )

        try:
            with urlopen(requisicao, timeout=15) as resposta:
                dados = json.loads(
                    resposta.read().decode("utf-8")
                )

        except HTTPError as erro:
            raise RuntimeError(
                f"Erro HTTP {erro.code} ao consultar a Deezer."
            ) from erro

        except (URLError, TimeoutError, OSError) as erro:
            raise RuntimeError(
                "Não foi possível conectar à Deezer."
            ) from erro

        except ValueError as erro:
            raise RuntimeError(
                "A Deezer retornou uma resposta inválida."
            ) from erro

        if "error" in dados:
            detalhe = dados["error"]

            if isinstance(detalhe, dict):
                detalhe = detalhe.get(
                    "message",
                    "Erro retornado pela Deezer."
                )

            raise RuntimeError(str(detalhe))

        artistas = dados.get("data", [])
        resultado = []

        for posicao, artista in enumerate(artistas[:20], start=1):

            resultado.append({
                "posicao": artista.get("position") or posicao,
                "nome": artista.get("name", "Artista desconhecido"),
                "ouvintes": 0,
                "reproducoes": 0,
                "foto": (
                    artista.get("picture_xl")
                    or artista.get("picture_big")
                    or artista.get("picture_medium")
                ),
                "url": artista.get("link")
            })

        return resultado
