import cloudinary
import cloudinary.uploader

from app.models.publicacao import Publicacao
from app.services.moderacaoService import moderarConteudo
from app.services.moderacaoImagemService import moderarImagem


class PublicacaoService:

    def __init__(self, repoPublicacao):
        self.repoPublicacao = repoPublicacao

    def criarPublicacao(
        self,
        arquivo,
        legenda,
        usuario_id,
        comunidade_id,
        tipo_midia
    ):
        # Modera o texto da publicação
        if legenda:
            permitido = moderarConteudo(legenda)

            if permitido is False:
                return "BLOQUEADO"

        # Modera imagens. Vídeos não passam por essa função.
        if tipo_midia == "imagem":
            imagem_permitida = moderarImagem(arquivo)

            if imagem_permitida is False:
                return "BLOQUEADO"

        try:
            # Garante que o arquivo seja lido desde o início
            arquivo.seek(0)

            # Envia a mídia para o Cloudinary
            resultado = cloudinary.uploader.upload(
                arquivo,
                resource_type=(
                    "video" if tipo_midia == "video" else "image"
                )
            )

            # Recupera a URL pública da mídia
            imagem_url = resultado["secure_url"]

        except Exception as e:
            print("Erro no Cloudinary:", e)
            return "ERRO"

        # Cria a publicação incluindo a URL da mídia
        novaPublicacao = Publicacao(
            usuario_id=usuario_id,
            comunidade_id=comunidade_id,
            legenda=legenda,
            tipo_midia=tipo_midia,
            imagem_url=imagem_url
        )

        # Salva a publicação no repositório
        try:
            return self.repoPublicacao.salvarPublicacao(novaPublicacao)
        except Exception as e:
            print("Erro ao salvar publicação no banco:", e)
            return "ERRO"

    def carregarPublicacao(self):
        return self.repoPublicacao.carregarPublicacoes()

    def apagarPublicacao(self, publicacao_id):
        return self.repoPublicacao.apagarPublicacao(publicacao_id)

    def buscarPublicacao(self, publicacao_id):
        return self.repoPublicacao.buscarPublicacao(publicacao_id)

    def carregarPublicacoesPorComunidade(self, comunidade_id):
        return self.repoPublicacao.carregarPublicacoesPorComunidade(
            comunidade_id
        )

    def listarFeedSeguindo(self, usuario_id):
        return self.repoPublicacao.listarFeedSeguindo(usuario_id)