from app.models.comentario import Comentario
from app.services.moderacaoService import moderarConteudo


class ComentarioService:

    def __init__(self, repoComentario):
        self.repoComentario = repoComentario


    def criarComentario(self, texto, usuario_id, publicacao_id):

        permitido = moderarConteudo(texto)

        if not permitido:
            return None

        novoComentario = Comentario(
            usuario_id=usuario_id,
            publicacao_id=publicacao_id,
            texto=texto
        )

        return self.repoComentario.salvarComentario(novoComentario)


    def carregarComentarios(self, publicacao_id):

        return self.repoComentario.carregarComentarios(
            publicacao_id
        )


    def editarComentario(self, comentario_id, usuario_id, texto):

        return self.repoComentario.editarComentario(
            comentario_id,
            usuario_id,
            texto
        )


    def apagarComentario(self, comentario_id, usuario_id):

        return self.repoComentario.apagarComentario(
            comentario_id,
            usuario_id
        )