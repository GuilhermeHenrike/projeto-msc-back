import cloudinary
import cloudinary.uploader
from app.models.publicacao import Publicacao
from app.services.moderacaoService import moderarConteudo
from app.services.moderacaoImagemService import moderarImagem


class PublicacaoService:

    def __init__(self, repoPublicacao):
        self.repoPublicacao = repoPublicacao

    def criarPublicacao(self, imagem, legenda, usuario_id, comunidade_id):

        if legenda:
            permitido = moderarConteudo(legenda)

            if permitido is False:
                return "BLOQUEADO"


        imagem_permitida = moderarImagem(imagem)

        if imagem_permitida is False:
            return "BLOQUEADO"


        try:
            imagem.seek(0)

            resultado = cloudinary.uploader.upload(imagem)

            imagem_url = resultado["secure_url"]

        except Exception as e:
            print("Erro no Cloudinary:", e)
            return "ERRO"

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

    def carregarPublicacoesPorComunidade(self, comunidade_id):
        return self.repoPublicacao.carregarPublicacoesPorComunidade(comunidade_id)