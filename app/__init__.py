
import os
from dotenv import load_dotenv
from flask import Flask, render_template, session, redirect
from flask_mail import Mail
import cloudinary

# Repositories
from app.repositories.authRepository import AuthRepository
from app.repositories.comunidadeRepository import ComunidadeRepository
from app.repositories.publicacaoRepository import PublicacaoRepository
from app.repositories.comentariosRepository import ComentarioRepository
from app.repositories.curtidaRepository import CurtidaRepository
from app.repositories.perfilRepository import PerfilRepository
from app.repositories.senhaRepository import SenhaRepository
from app.repositories.albumRepository import AlbumRepository
from app.repositories.albumSalvoRepository import AlbumSalvoRepository
from app.repositories.avaliacaoRepository import AvaliacaoRepository
from app.repositories.composicaoRepository import ComposicaoRepository

# Services
from app.services.authService import AuthService
from app.services.comunidadeService import ComunidadeService
from app.services.publicacaoService import PublicacaoService
from app.services.comentarioService import ComentarioService
from app.services.curtidaService import CurtidaService
from app.services.perfilService import PerfilService
from app.services.senhaService import SenhaService
from app.services.albumService import AlbumService
from app.services.avaliacaoService import AvaliacaoService
from app.services.composicaoService import ComposicaoService
from app.services.artistasService import ArtistasService

from flask_cors import CORS

# Controllers
from app.controllers.authController import authController
from app.controllers.comunidadeController import comunidadeController
from app.controllers.publicacaoController import publicacaoController
from app.controllers.comentarioController import comentarioController
from app.controllers.curtidaController import curtidaController
from app.controllers.perfilController import perfilController
from app.controllers.senhaController import senhaController
from app.controllers.albumController import albumController
from app.controllers.avaliacaoController import avaliacaoController
from app.controllers.composicaoController import composicaoController
from app.controllers.artistasController import artistasController


def create_app():

    app = Flask(__name__)

    CORS(
        app,
        origins=["http://localhost:5173"],
        supports_credentials=True
    )

    load_dotenv()

    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )

    mail = Mail()
    app.config["SECRET_KEY"] = "aaa"
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "nyedsomwander@gmail.com"
    app.config["MAIL_PASSWORD"] = "kjes ebpr hoxp ertu"
    app.config["MAIL_DEFAULT_SENDER"] = "nyedsomwander@gmail.com"

    mail.init_app(app)

    # =========================
    # REPOSITORIES
    # =========================

    repoAuth = AuthRepository()
    repoComunidade = ComunidadeRepository()
    repoPublicacao = PublicacaoRepository()
    repoPerfil = PerfilRepository()
    comentarioRepository = ComentarioRepository()
    curtidaRepository = CurtidaRepository()
    repoSenha = SenhaRepository()
    repoAlbum = AlbumRepository()
    repoAlbumSalvo = AlbumSalvoRepository()
    repoAvaliacao = AvaliacaoRepository()
    repoComposicao = ComposicaoRepository()

    # =========================
    # SERVICES
    # =========================

    authService = AuthService(repoAuth)
    comunidadeService = ComunidadeService(repoComunidade)
    publicacaoService = PublicacaoService(repoPublicacao)
    comentarioService = ComentarioService(comentarioRepository)
    curtidaService = CurtidaService(curtidaRepository)
    senhaService = SenhaService(repoSenha, repoAuth, mail)
    albumService = AlbumService(repoAlbum, repoAlbumSalvo)
    avaliacaoService = AvaliacaoService(repoAvaliacao)
    perfilService = PerfilService(repoPerfil, avaliacaoService)
    composicaoService = ComposicaoService(repoComposicao)

    # =========================
    # CONTROLLERS
    # =========================

    authController(app, authService)
    comunidadeController(app, comunidadeService)
    perfilController(app, perfilService)
    publicacaoController(app, publicacaoService)
    comentarioController(app, comentarioService)
    curtidaController(app, curtidaService)
    senhaController(app, senhaService)
    albumController(app, albumService)
    avaliacaoController(app, avaliacaoService)
    composicaoController(app, composicaoService)

    # =========================
    # ARTISTAS EM ALTA
    # =========================

    artistasService = ArtistasService()
    artistasController(app, artistasService)

    @app.route("/")
    def login():
        return render_template("Login.html")

    @app.route("/registro")
    def registroPage():
        return render_template("Registro.html")

    @app.route("/home")
    def homePage():

        if "user.id" not in session:
            return redirect("/")

        usuario_id = session["user.id"]

        comunidades = comunidadeService.listarTodasComunidadesDoUsuario(
            usuario_id
        )
        publicacoes = publicacaoService.carregarPublicacao()

        for publicacao in publicacoes:
            publicacao["comentarios"] = comentarioService.carregarComentarios(
                publicacao["id"]
            )

            publicacao["curtidas"] = curtidaService.contarCurtidas(
                publicacao["id"]
            )

        return render_template(
            "Home.html",
            comunidades=comunidades,
            publicacoes=publicacoes
        )

    @app.route("/enviar-codigo")
    def envCod():
        return render_template("env_cod.html")

    @app.route("/confirmar-codigo")
    def confCodPage():
        return render_template("conf-cod.html")

    @app.route("/validar-cod")
    def validarCodePage():
        return render_template("validar-cod.html")

    @app.route("/mudar-senha")
    def mudarSenhaPage():
        return render_template("mudar-senha.html")

    @app.route("/criar-publicao")
    def criarPublicacaoPage():

        if "user.id" not in session:
            return redirect("/")

        return render_template("publicacao.html")

    @app.route("/entrarSairComunidade")
    def entrarSair():

        if "user.id" not in session:
            return redirect("/")

        usuario_id = session["user.id"]

        comunidadesDisponiveis = (
            comunidadeService.listarComunidadesNaoParticipa(usuario_id)
        )

        return render_template(
            "entrarSairComunidade.html",
            comunidades=comunidadesDisponiveis
        )

    return app
