import cloudinary
import cloudinary.uploader

from app.models.publicacao import Publicacao
from app.services.moderacaoService import (
    moderarConteudo,
    moderarLegenda
)


class PublicacaoService:

    def __init__(self, repoPublicacao, repoComunidade):
        self.repoPublicacao = repoPublicacao
        self.repoComunidade = repoComunidade

    def criarPublicacao(
        self,
        arquivo,
        legenda,
        usuario_id,
        comunidade_id,
        tipo_midia
    ):
        try:

            # Verifica se o não usuario faz parte da comunidade
            if not self.repoComunidade.usuarioParticipa(
                usuario_id,
                comunidade_id
            ):
                return "NAO_PARTICIPA"

            # Verifica se o arquivo foi enviado
            if arquivo is None or not arquivo.filename:
                return "DADOS_INVALIDOS"

            # Lê o conteúdo do arquivo
            arquivo_bytes = arquivo.read()

            if not arquivo_bytes:
                return "DADOS_INVALIDOS"

            # Moderação do conteúdo
            try:
                if tipo_midia == "imagem":
                    # Modera a legenda e a imagem
                    permitido = moderarConteudo(
                        legenda,
                        arquivo_bytes,
                        arquivo.mimetype
                    )

                elif tipo_midia == "video":
                    # Modera a legenda do vídeo
                    # O vídeo em si não é analisado visualmente aqui
                    permitido = moderarLegenda(legenda)

                else:
                    return "DADOS_INVALIDOS"

            except ValueError as erro:
                print("Dados inválidos:", erro)
                return "DADOS_INVALIDOS"

            except Exception as erro:
                print("Falha na moderação:", repr(erro))
                return "ERRO_MODERACAO"

            # Bloqueia conteúdos reprovados
            if permitido is not True:
                return "BLOQUEADO"

            # Volta o arquivo ao início antes do upload
            arquivo.seek(0)

            # Envia a imagem ou o vídeo ao Cloudinary
            resultado = cloudinary.uploader.upload(
                arquivo,
                resource_type=(
                    "video" if tipo_midia == "video" else "image"
                )
            )

            imagem_url = resultado["secure_url"]

            # Monta a publicação
            novaPublicacao = Publicacao(
                usuario_id=usuario_id,
                comunidade_id=comunidade_id,
                legenda=legenda,
                tipo_midia=tipo_midia,
                imagem_url=imagem_url
            )

            # Salva no banco de dados
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

    def listarFeedSeguindo(self, usuario_id):
        return self.repoPublicacao.listarFeedSeguindo(usuario_id)
