from flask import redirect, request, session
from mysql.connector.errors import IntegrityError

def authController(app, authService):

    @app.route("/registro", methods=["POST"])
    def registro():
        dados = request.get_json()
        nome = dados.get("nome")
        email = dados.get("email")
        senha = dados.get("senha")

        try:
            authService.fazerRegistro(nome, email, senha)
            return {"message": "Usuário registrado com sucesso"}, 201
        
        except IntegrityError:
            return {"error": "Este email já está cadastrado"}, 409

    
    @app.route("/logar", methods=["POST"])
    def logar():
        dados = request.get_json()
        email = dados.get("email")
        senha = dados.get("senha")

        user = authService.fazerLogin(email, senha)

        if user:
            session["user.id"] = user.id
            return {"message": "Login realizado com sucesso"}, 200

        return {"error": "Email ou senha incorretos"}, 401


    @app.route("/logout", methods=["POST"])
    def logout():
        session.clear()

        return {"message": "Logout realizado com sucesso"}, 200 


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
    

        