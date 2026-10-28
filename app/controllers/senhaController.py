from flask import request, session

def senhaController(app, senhaService):

    @app.route("/enviar-codigo", methods=["POST"])
    def enviarCodigo():
        dados = request.get_json()
        email = dados.get("email")

        senhaService.enviarCodigo(email)

        return "codigo enviado!"


    @app.route("/conf-codigo", methods=["POST"])
    def confirmarCodigo():
        dados = request.get_json()
        codigo_digitado = dados.get("codigo")

        cod_validado = senhaService.confirmarCodigo(codigo_digitado)

        if cod_validado == True:
            return "Código confirmado"

        return "Código não compatível."


    @app.route("/mudar-senha", methods=["POST"])
    def mudarSenha():
        dados = request.get_json()

        nova_senha = dados.get("novasenha")
        email = session.get("email_recuperacao")

        if not nova_senha:
            return "digite uma nova senha"

        sucesso = senhaService.mudarSenha(nova_senha, email)

        if sucesso:
            return "senha atualizada com sucesso"

        return "nao foi possivel atualizar sua senha"


    @app.route("/mudar-senha-perfil", methods=["POST"])
    def mudarSenhaPerfil():
        dados = request.get_json()

        nova_senha = dados.get("novasenha")
        usuario_id = session.get("user.id")

        if not nova_senha:
            return "digite uma nova senha"

        sucesso = senhaService.mudarSenhaPerfil(
            nova_senha,
            usuario_id
        )

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

        resultado = senhaService.confirmarSenhaAtual(usuario_id, senha)

        if resultado:
            return "Senha confirmada", 200

        return "Senha incorreta", 401