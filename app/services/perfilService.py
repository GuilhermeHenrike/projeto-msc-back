from app.models.usuario import Usuario

class PerfilService:

    def __init__(self, repoPerfil):
        self.repoPerfil = repoPerfil

    def buscarPerfil(self, usuario_id):

        return self.repoPerfil.buscarPerfil(usuario_id)


    def atualizarPerfil(self, nome, imagem_url, usuario_id):

        usuarioAtualizado = Usuario(nome, None, None, id=usuario_id, foto_url=imagem_url)
        return self.repoPerfil.editarPerfil(usuarioAtualizado)