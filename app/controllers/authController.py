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

    @app.route("/logout", methods=["POST"])
    def logout():
        session.clear()

        return redirect("/")   

    @app.route("/enviar-codigo", methods = ["POST"])
    def enviarCodigo():

        email = request.form.get("email")
        authService.enviarCodigo(email)

        return redirect("/confirmar-codigo")

    @app.route("/conf-codigo", methods=["POST"])
    def confirmarCodigo():

        codigo_digitado = request.form.get("codigo")

        cod_validado = authService.confirmarCodigo(codigo_digitado)

        if cod_validado == True:
            return redirect("/mudar-senha")
        else:
            return "Código não compatível."

    @app.route("/mudar-senha", methods = ["POST"])
    def mudarSenha():

        nova_senha = request.form.get("novasenha")
        email = session.get("email_recuperacao")

        if not nova_senha:
            return "digite uma nova senha"
        
        sucesso = authService.mudarSenha(nova_senha, email)

        if sucesso:
            return redirect("/")

        return "nao foi possivel atualizar sua senha"
    

        