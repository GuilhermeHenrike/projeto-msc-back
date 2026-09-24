from app.models.usuario import Usuario

class PerfilService:

    def __init__(self, repoPerfil):
        self.repoPerfil = repoPerfil

    def atualizarPerfil(self, nome, imagem_url, usuario_id):

        usuarioAtualizado = Usuario(nome, None, None, id=usuario_id, foto_url=imagem_url)
        return self.repoPerfil.editarPerfil(usuarioAtualizado)

    def buscarPerfil(self, usuario_id):

        usuario = self.repoPerfil.buscarUsuario(usuario_id)

        if not usuario:
            return None

        publicacoes = self.repoPerfil.buscarPublicacoesUsuario(usuario_id)

        return {
            "usuario": usuario,
            "publicacoes": publicacoes
        }