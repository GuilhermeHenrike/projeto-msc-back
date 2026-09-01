from flask import redirect, request, session


def publicacaoController(app, publicacaoService):

    @app.route("/publicacao", methods=["POST"])
    def criarPublicacao():

        if "user.id" not in session:
            return redirect("/")

        imagem = request.files.get("imagem")
        legenda = request.form.get("legenda")
        comunidade_id = request.form.get("comunidade")

        if not imagem:
            return "selecione uma imagem"

        usuario_id = session["user.id"]

        publicacao = publicacaoService.criarPublicacao(
            imagem,
            legenda,
            usuario_id,
            comunidade_id
        )

        if publicacao is None:
            return "Sua publicação foi bloqueada por conter conteúdo inadequado", 400

        return redirect("/home")


    @app.route("/apagar-publicacao/<int:id>", methods=["DELETE"])
    def apagarPublicacao(id):

        if "user.id" not in session:
            return "Usuário não está logado", 401

        publicacao = publicacaoService.buscarPublicacao(id)

        if publicacao is None:
            return "Publicação não encontrada", 404

        if publicacao["usuario_id"] != session["user.id"]:
            return "Você não pode apagar essa publicação", 403

        publicacaoService.apagarPublicacao(id)

        return "", 204