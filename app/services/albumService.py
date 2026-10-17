import requests

from app.models.album import Album


class AlbumService:

    def __init__(self, repoAlbum, repoAlbumSalvo):
        self.repoAlbum = repoAlbum
        self.repoAlbumSalvo = repoAlbumSalvo

    def buscarAlbunsDeezer(self, query):

        if not query or not query.strip():
            return []

        try:
            resposta = requests.get(
                "https://api.deezer.com/search/album",
                params={"q": query.strip()},
                timeout=10
            )

            if resposta.status_code >= 400:
                raise requests.HTTPError("Erro ao consultar a Deezer.")
        
            dados = resposta.json().get("data", [])

            return [
                {
                    "deezer_id": album["id"],
                    "titulo": album.get("title", ""),
                    "artista": album.get("artist", {}).get("name", ""),
                    "capa_url": album.get("cover_medium", "")
                }
                for album in dados
            ]

        except requests.RequestException as erro:
            print("Erro ao consultar Deezer:", erro)
            raise RuntimeError("Não foi possível consultar a Deezer.")


    def salvarAlbumUsuario(self, usuario_id, dados_album):

        deezer_id = dados_album.get("deezer_id")

        if not deezer_id:
            raise ValueError("ID do álbum inválido.")

        albumNoBanco = self.repoAlbum.buscarAlbumPorDeezerId(deezer_id)

        if not albumNoBanco:
            novo_album = Album(
                deezer_id=deezer_id,
                titulo=dados_album["titulo"],
                artista=dados_album["artista"],
                capa_url=dados_album["capa_url"]
            )

            album = self.repoAlbum.salvarAlbum(novo_album)
        else:
            album = albumNoBanco


        if isinstance(album, dict):
            album_id = album["id"]
        else:
            album_id = album.id

        self.repoAlbumSalvo.salvarAlbumUsuario(usuario_id, album_id)

        return album


    def carregarAlbunsSalvos(self, usuario_id):
        return self.repoAlbumSalvo.carregarAlbunsSalvos(usuario_id)


    def removerAlbumUsuario(self, usuario_id, album_id):
        return self.repoAlbumSalvo.removerAlbumUsuario(usuario_id, album_id)