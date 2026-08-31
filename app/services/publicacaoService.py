import cloudinary
import cloudinary.uploader
from app.models.publicacao import Publicacao


class PublicacaoService:

    def __init__(self, repoPublicacao):
        self.repoPublicacao = repoPublicacao

    def criarPublicacao(self, imagem, legenda, usuario_id, comunidade_id):
        # Envia a imagem para o Cloudinary
        resultado = cloudinary.uploader.upload(imagem)

        # Pega a URL segura HTTPS retornada
        imagem_url = resultado["secure_url"]

        # Instancia e salva a publicação
        novaPublicacao = Publicacao(
            usuario_id=usuario_id,
            comunidade_id=comunidade_id,
            legenda=legenda,
            imagem_url=imagem_url,
        )

        return self.repoPublicacao.salvarPublicacao(novaPublicacao)

    def carregarPublicacao(self):

        return self.repoPublicacao.carregarPublicacoes()