from flask import Flask, render_template, session, redirect

from app.controllers.authController import authController
from app.controllers.comunidadeController import comunidadeController
from app.controllers.publicacaoController import publicacaoController

from app.repositories.authRepository import AuthRepository
from app.repositories.comunidadeRepository import ComunidadeRepository
from app.repositories.publicacaoRepository import PublicacaoRepository

from app.services.authService import AuthService
from app.services.comunidadeService import ComunidadeService
from app.services.publicacaoService import PublicacaoService

from flask_mail import Mail

import os
from dotenv import load_dotenv
import cloudinary

def create_app():

    app = Flask(__name__)

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


    repoUser = AuthRepository()
    repoComunidade = ComunidadeRepository()
    repoPublicacao = PublicacaoRepository()

    authService = AuthService(repoUser, mail)
    comunidadeService = ComunidadeService(repoComunidade)
    publicacaoService = PublicacaoService(repoPublicacao)

    authController(app, authService)
    comunidadeController(app, comunidadeService)
    publicacaoController(app, publicacaoService)

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

        return render_template(
            "Home.html",
            comunidades=comunidades
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

    return app