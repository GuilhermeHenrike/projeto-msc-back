
import cloudinary
import cloudinary.uploader

from app.models.publicacao import Publicacao
from app.services.moderacaoService import moderarConteudo


class PublicacaoService:

    def __init__(self, repoPublicacao):
        self.repoPublicacao = repoPublicacao

    def criarPublicacao(
        self,
        imagem,
        legenda,
        usuario_id,
        comunidade_id
    ):
        try:
            if imagem is None:
                return "DADOS_INVALIDOS"

            imagem_bytes = imagem.read()

            try:
                permitido = moderarConteudo(
                    legenda,
                    imagem_bytes,
                    imagem.mimetype
                )

            except ValueError as erro:
                print("Dados inválidos:", erro)
                return "DADOS_INVALIDOS"

            except Exception as erro:
                print("Falha na moderação:", repr(erro))
                return "ERRO_MODERACAO"

            if permitido is not True:
                return "BLOQUEADO"

            imagem.seek(0)

            resultado = cloudinary.uploader.upload(
                imagem,
                resource_type="image"
            )

            imagem_url = resultado["secure_url"]

            novaPublicacao = Publicacao(
                usuario_id=usuario_id,
                comunidade_id=comunidade_id,
                legenda=legenda,
                imagem_url=imagem_url
            )

            publicacao_salva = (
                self.repoPublicacao.salvarPublicacao(
                    novaPublicacao
                )
            )

            if not publicacao_salva:
                return "ERRO"

            return publicacao_salva

        except Exception as erro:
            print("Erro ao criar publicação:", repr(erro))
            return "ERRO"

    def carregarPublicacao(self):
        return self.repoPublicacao.carregarPublicacoes()

    def apagarPublicacao(self, publicacao_id):
        return self.repoPublicacao.apagarPublicacao(
            publicacao_id
        )

    def buscarPublicacao(self, publicacao_id):
        return self.repoPublicacao.buscarPublicacao(
            publicacao_id
        )

    def carregarPublicacoesPorComunidade(self, comunidade_id):
        return self.repoPublicacao.carregarPublicacoesPorComunidade(
            comunidade_id
        )
