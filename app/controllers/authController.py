from flask import redirect, request, session

def authController(app, authService):

    @app.route("/registro", methods=["POST"])
    def registro():
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        authService.fazerRegistro(nome, email, senha)

        return redirect("/")

    @app.route("/logar", methods=["POST"])
    def logar():
        email = request.form.get("email")
        senha = request.form.get("senha")

        user = authService.fazerLogin(email, senha)

        if user:
            session["user.id"] = user.id
            return redirect("/home")

        return "Nome ou senha incorretos", 401