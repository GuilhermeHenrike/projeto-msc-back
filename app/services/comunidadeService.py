from app.models.comunidade import Comunidade

class ComunidadeService:

    def __init__(self, repoComunidade):
        self.repoComunidade = repoComunidade


    def criarComunidade(self, nome, genero, criador_id, descricao, imagem_url):

        novaComunidade = Comunidade(nome, genero, criador_id, descricao, imagem_url)
        return self.repoComunidade.salvarComunidade(novaComunidade)


    def atualizarComunidade(self, nome, genero, descricao, imagem_url, comunidade_id):

        comunidadeAtualizada = Comunidade(nome, genero=genero, descricao=descricao, imagem_url=imagem_url, id=comunidade_id)
        return self.repoComunidade.editarComunidade(comunidadeAtualizada, comunidade_id)


    def apagarComunidade(self, comunidade_id):

        return self.repoComunidade.apagarComunidade(comunidade_id)


    ## PROCURAR COMUNIDADES:


    def listarComunidadesNaoParticipa(self, usuario_id):

        return self.repoComunidade.todasComunidades(usuario_id)


    def listarComunidade(self, comunidade_id):

        return self.repoComunidade.buscarComunidade(comunidade_id)


    def listarTodasComunidadesDoUsuario(self, usuario_id):

        return self.repoComunidade.todasComunidadesPorUsuario(usuario_id)


    ## FILTRO


    def filtroComunidadesPorGenero(self, genero):

        return self.repoComunidade.comunidadesPorGenero(genero)


    ## ENTRAR E SAIR


    def entrarComunidade(self, usuario_id, comunidade_id):

        return self.repoComunidade.entrarComunidade(usuario_id, comunidade_id)
    

    def sairComunidade(self, usuario_id, comunidade_id):

        return self.repoComunidade.sairComunidade(usuario_id, comunidade_id)