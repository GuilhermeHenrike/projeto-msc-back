from flask import Flask

def create_app():
    app = Flask(__name__)

    # Registra os controllers/blueprints aqui
    # from app.controllers.auth_controller import auth_bp
    # app.register_blueprint(auth_bp)

    return app