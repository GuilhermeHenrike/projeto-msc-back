from flask import Flask, render_template
from app.controllers.authController import authController
from app.repositories.authRepository import AuthRepository
from app.services.authService import AuthService

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "aaa"

    repoUser = AuthRepository()
    
    authService = AuthService(repoUser)

    @app.route("/")
    def login(): 
        return render_template("Login.html")

    @app.route("/registro")
    def registroPage():
        return render_template("Registro.html")

    @app.route("/home")
    def homePage():
        return render_template("Home.html")

    authController(app, authService)


    return app