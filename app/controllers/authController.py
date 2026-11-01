from flask import request, session, jsonify
from mysql.connector.errors import IntegrityError


def authController(app, authService):

    @app.route("/registro", methods=["POST"])
    def registro():
        dados = request.get_json()
        nome = dados.get("nome")
        email = dados.get("email")
        senha = dados.get("senha")

        try:
            resultado = authService.fazerRegistro(nome, email, senha)

            if resultado == "SENHA_CURTA":
                return jsonify({
                    "erro": "A senha deve ter pelo menos 8 caracteres."
                }), 400

            return {"mensagem": "Usuário registrado com sucesso"}, 201

        except IntegrityError:
            return {"erro": "Este email já está cadastrado"}, 409

    @app.route("/logar", methods=["POST"])
    def logar():
        dados = request.get_json()
        email = dados.get("email")
        senha = dados.get("senha")

        user = authService.fazerLogin(email, senha)

        if user:
            session["user.id"] = user.id
            return {"mensagem": "Login realizado com sucesso"}, 200

        return {"erro": "Email ou senha incorretos"}, 401


    @app.route("/logout", methods=["POST"])
    def logout():
        session.clear()
        return {"mensagem": "Logout realizado com sucesso"}, 200