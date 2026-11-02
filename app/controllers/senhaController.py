from flask import request, session


def senhaController(app, senhaService):

    @app.route("/enviar-codigo", methods=["POST"])
    def enviarCodigo():
        dados = request.get_json()

        if not dados:
            return "Dados não informados", 400

        email = dados.get("email")

        if not email:
            return "Informe o e-mail", 400

        sucesso = senhaService.enviarCodigo(email)

        if sucesso:
            return "Código enviado!", 200

        return "Não foi possível enviar o código. Verifique o e-mail ou tente novamente.", 400

    @app.route("/confirmar-codigo", methods=["POST"])
    def confirmarCodigo():
        dados = request.get_json()

        if not dados:
            return "Dados não informados", 400

        codigo = dados.get("codigo")

        if not codigo:
            return "Informe o código", 400

        sucesso = senhaService.confirmarCodigo(codigo)

        if sucesso:
            return "Código confirmado!", 200

        return "Código não compatível", 400

    @app.route("/mudar-senha", methods=["POST"])
    def mudarSenha():
        dados = request.get_json()

        if not dados:
            return "Dados não informados", 400

        nova_senha = dados.get("novasenha")
        email = session.get("email_recuperacao")

        if not nova_senha:
            return "Digite uma nova senha", 400

        sucesso = senhaService.mudarSenha(nova_senha, email)

        if sucesso:
            return "Senha atualizada com sucesso", 200

        return "Não foi possível atualizar sua senha", 400

    @app.route("/mudar-senha-perfil", methods=["POST"])
    def mudarSenhaPerfil():
        dados = request.get_json()

        if not dados:
            return "Dados não informados", 400

        nova_senha = dados.get("novasenha")
        usuario_id = session.get("user.id")

        if not nova_senha:
            return "Digite uma nova senha", 400

        sucesso = senhaService.mudarSenhaPerfil(
            nova_senha,
            usuario_id
        )

        if sucesso:
            return "Senha atualizada com sucesso", 200

        return "Não foi possível atualizar sua senha", 400

    @app.route("/confirmar-senha", methods=["POST"])
    def confirmarSenha():
        if "user.id" not in session:
            return "Usuário não autenticado", 401

        dados = request.get_json()

        if not dados:
            return "Dados não informados", 400

        senha = dados.get("senha")
        usuario_id = session["user.id"]

        if not senha:
            return "Informe a senha", 400

        resultado = senhaService.confirmarSenhaAtual(
            usuario_id,
            senha
        )

        if resultado:
            return "Senha confirmada", 200

        return "Senha incorreta", 401