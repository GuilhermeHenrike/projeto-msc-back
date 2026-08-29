from flask import Flask, render_template, session, redirect
from app.controllers.authController import authController
from app.controllers.comunidadeController import comunidadeController
from app.repositories.authRepository import AuthRepository
from app.repositories.comunidadeRepository import ComunidadeRepository
from app.services.authService import AuthService
from app.services.comunidadeService import ComunidadeService


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "aaa"

    repoUser = AuthRepository()
    repoComunidade = ComunidadeRepository()
    
    authService = AuthService(repoUser)
    comunidadeService = ComunidadeService(repoComunidade)

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
        comunidades = comunidadeService.listarTodasComunidadesDoUsuario(usuario_id)
        return render_template("Home.html", comunidades=comunidades)

    authController(app, authService)
    comunidadeController(app, comunidadeService)

    return app