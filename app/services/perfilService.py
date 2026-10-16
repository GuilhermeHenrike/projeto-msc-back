from app.models.usuario import Usuario
import cloudinary
import cloudinary.uploader

class PerfilService:

    def __init__(self, repoPerfil):
        self.repoPerfil = repoPerfil


    def atualizarPerfil(self, nome, usuario_id, foto_perfil=None, foto_url_background=None
    ):
        imagem_url = None

        if foto_perfil:
            resultado = cloudinary.uploader.upload(foto_perfil, folder="yrplace/perfis")
            imagem_url = resultado["secure_url"]

        if foto_url_background:
            resultado = cloudinary.uploader.upload(foto_url_background, folder="yrplace/capas")
            foto_url_background = resultado["secure_url"]

        usuarioAtualizado = Usuario(nome, None, None, id=usuario_id, foto_url=imagem_url, foto_url_background=foto_url_background)

        return self.repoPerfil.editarPerfil(usuarioAtualizado)



    def buscarPerfilComDados(self, usuario_id):

        usuario = self.repoPerfil.buscarUsuario(usuario_id)

        if not usuario:
            return None

        publicacoes = self.repoPerfil.buscarPublicacoesUsuario(usuario_id)

        return {
            "usuario": usuario,
            "publicacoes": publicacoes
        }


    def buscarPerfil(self, usuario_id):

        usuario = self.repoPerfil.buscarUsuario(usuario_id)
        return usuario
