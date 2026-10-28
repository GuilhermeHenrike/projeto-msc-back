from app.models.comentario import Comentario


class ComentarioService:

    def __init__(self, repoComentario):
        self.repoComentario = repoComentario


    def criarComentario(self, texto, usuario_id, publicacao_id):

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