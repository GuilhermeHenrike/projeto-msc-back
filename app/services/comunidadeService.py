from app.models.comunidade import Comunidade

class ComunidadeService:

    def __init__(self, repoComunidade):
        self.repoComunidade = repoComunidade

    def criarComunidade(self, nome, criador_id, descricao, imagem_url):

        novaComunidade = Comunidade(nome, criador_id, descricao, imagem_url)
        return self.repoComunidade.salvarComunidade(novaComunidade)

    def atualizarComunidade(self, nome, descricao, imagem_url, comunidade_id):

        comunidadeAtualizada = Comunidade(nome, descricao=descricao, imagem_url=imagem_url, id=comunidade_id)
        return self.repoComunidade.editarComunidade(comunidadeAtualizada, comunidade_id)

    def apagarComunidade(self, comunidade_id):

        return self.repoComunidade.apagarComunidade(comunidade_id)

    ## PROCURAR COMUNIDADES:

    def listarTodasComunidades(self):

        return self.repoComunidade.todasComunidades()

    def listarComunidade(self, comunidade_id):

        return self.repoComunidade.buscarComunidade(comunidade_id)

    def listarTodasComunidadesDoUsuario(self, usuario_id):

        return self.repoComunidade.todasComunidadesPorUsuario(usuario_id)