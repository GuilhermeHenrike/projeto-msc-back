import cloudinary
import cloudinary.uploader
from app.models.publicacao import Publicacao


class PublicacaoService:

    def __init__(self, repoPublicacao):
        self.repoPublicacao = repoPublicacao


    def criarPublicacao(self, imagem, legenda, usuario_id, comunidade_id):

        resultado = cloudinary.uploader.upload(imagem)

        imagem_url = resultado["secure_url"]

        novaPublicacao = Publicacao(
            usuario_id=usuario_id,
            comunidade_id=comunidade_id,
            legenda=legenda,
            imagem_url=imagem_url
        )

        return self.repoPublicacao.salvarPublicacao(novaPublicacao)


    def carregarPublicacao(self):

        return self.repoPublicacao.carregarPublicacoes()


    def apagarPublicacao(self, publicacao_id):

        return self.repoPublicacao.apagarPublicacao(publicacao_id)


    def buscarPublicacao(self, publicacao_id):

        return self.repoPublicacao.buscarPublicacao(publicacao_id)