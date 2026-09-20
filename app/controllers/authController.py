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


    @app.route("/enviar-codigo", methods = ["POST"])
    def enviarCodigo():

        dados = request.get_json()
        email = dados.get("email")
        authService.enviarCodigo(email)

        return "codigo enviado!"

    @app.route("/conf-codigo", methods=["POST"])
    def confirmarCodigo():

        dados = request.get_json()

        codigo_digitado = dados.get("codigo")

        cod_validado = authService.confirmarCodigo(codigo_digitado)

        if cod_validado == True:
            return "Código confirmado"
        else:
            return "Código não compatível."

    @app.route("/mudar-senha", methods = ["POST"])
    def mudarSenha():

        dados = request.get_json()

        nova_senha = dados.get("novasenha")
        email = session.get("email_recuperacao")

        if not nova_senha:
            return "digite uma nova senha"
        
        sucesso = authService.mudarSenha(nova_senha, email)

        if sucesso:
            return "senha atualizada com sucesso"

        return "nao foi possivel atualizar sua senha"
    

    @app.route("/confirmar-senha", methods=["POST"])
    def confirmarSenha():

        if "user.id" not in session:
            return "Usuário não autenticado", 401

        dados = request.get_json()

        senha = dados.get("senha")
        usuario_id = session["user.id"]

        resultado = authService.confirmarSenhaAtual(usuario_id, senha)

        if resultado:
            return "Senha confirmada", 200

        return "Senha incorreta", 401