import os
from dotenv import load_dotenv
from flask import Flask, session
from flask_mail import Mail
import cloudinary
from flask_cors import CORS

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
from app.repositories.notificacaoRepository import NotificacaoRepository

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
from app.services.notificacaoService import NotificacaoService

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
from app.controllers.notificacaoController import notificacaoController


def create_app():

    app = Flask(__name__)

    CORS(
        app,
        origins=[
            "http://localhost:5173",
            "https://yrplace-git-deploy-wanderxrs.vercel.app"
        ],
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

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = True

    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT") or "587")
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

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
    repoNotificacao = NotificacaoRepository()

    # =========================
    # SERVICES
    # =========================

    authService = AuthService(repoAuth)
    comunidadeService = ComunidadeService(repoComunidade)
    publicacaoService = PublicacaoService(repoPublicacao, repoComunidade)
    comentarioService = ComentarioService(comentarioRepository)
    curtidaService = CurtidaService(curtidaRepository)
    senhaService = SenhaService(repoSenha, repoAuth)
    albumService = AlbumService(repoAlbum, repoAlbumSalvo)
    avaliacaoService = AvaliacaoService(repoAvaliacao)
    perfilService = PerfilService(repoPerfil, avaliacaoService)
    composicaoService = ComposicaoService(repoComposicao)
    notificacaoService = NotificacaoService(repoNotificacao)

    # =========================
    # CONTROLLERS
    # =========================

    authController(app, authService)
    comunidadeController(app, comunidadeService)
    perfilController(app, perfilService)
    publicacaoController(app, publicacaoService)
    senhaController(app, senhaService)
    albumController(app, albumService)
    avaliacaoController(app, avaliacaoService)
    composicaoController(app, composicaoService)
    comentarioController(app, comentarioService, notificacaoService)
    curtidaController(app, curtidaService, notificacaoService)
    notificacaoController(app, notificacaoService)

    # =========================
    # ARTISTAS EM ALTA
    # =========================

    artistasService = ArtistasService()
    artistasController(app, artistasService)

    return app