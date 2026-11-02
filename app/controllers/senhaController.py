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