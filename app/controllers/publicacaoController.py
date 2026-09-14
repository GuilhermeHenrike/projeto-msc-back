from flask import redirect, request, session


def publicacaoController(app, publicacaoService):

    @app.route("/publicacao", methods=["POST"])
    def criarPublicacao():

        if "user.id" not in session:
            return redirect("/")

        dados = request.get_json()
        imagem = dados.get("imagem")
        legenda = dados.get("legenda")
        comunidade_id = dados.get("comunidade")

        if not imagem:
            return "selecione uma imagem"
        

        usuario_id = session["user.id"]

        publicacaoService.criarPublicacao(
            imagem,
            legenda,
            usuario_id,
            comunidade_id
        )

        return "Publicação enviada"


    @app.route("/apagar-publicacao/<int:id>", methods=["DELETE"])
    def apagarPublicacao(id):

        if "user.id" not in session:
            return "Usuário não está logado"

        publicacao = publicacaoService.buscarPublicacao(id)

        if publicacao is None:
            return "Publicação não encontrada"

        if publicacao["usuario_id"] != session["user.id"]:
            return "Você não pode apagar essa publicação"

        publicacaoService.apagarPublicacao(id)

        return "", 204