from flask import Flask, render_template
from app.controllers.authController import authController
from app.repositories.authRepository import AuthRepository
from app.services.authService import AuthService
from flask_mail import Mail


def create_app():

    app = Flask(__name__)

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

    authService = AuthService(repoUser, mail)


    @app.route("/")
    def login():
        return render_template("Login.html")


    @app.route("/registro")
    def registroPage():
        return render_template("Registro.html")


    @app.route("/home")
    def homePage():
        return render_template("Home.html")

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

    authController(app, authService)


    return app