from app.models.avaliacao import Avaliacao


class AvaliacaoService:
    def __init__(self, repoAvaliacao):
        self.repoAvaliacao = repoAvaliacao


    def validarNota(self, nota):
        try:
            nota = float(nota)
        except (ValueError, TypeError):
            raise ValueError("A nota deve ser um número.")

        if nota < 0 or nota > 10:
            raise ValueError("A nota deve estar entre 0 e 10.")

        return nota


    def salvarAvaliacao(self, usuario_id, album_id, nota):

        nota = self.validarNota(nota)

        avaliacao_existente = self.repoAvaliacao.buscarAvaliacao(usuario_id, album_id)

        if avaliacao_existente:
            raise ValueError("Você já avaliou esse álbum. Edite sua avaliação.")

        avaliacao = Avaliacao(usuario_id=usuario_id, album_id=album_id, nota=nota)

        return self.repoAvaliacao.salvarAvaliacao(avaliacao)


    def editarAvaliacao(self, usuario_id, album_id, nota):
        nota = self.validarNota(nota)

        avaliacao = self.repoAvaliacao.buscarAvaliacao(usuario_id, album_id)

        if not avaliacao:
            raise ValueError("Você ainda não avaliou esse álbum.")

        self.repoAvaliacao.atualizarAvaliacao(usuario_id, album_id, nota)

        return self.repoAvaliacao.buscarAvaliacao(usuario_id, album_id)


    def carregarAvaliacoesUsuario(self, usuario_id):
        return self.repoAvaliacao.carregarAvaliacoesUsuario(usuario_id)