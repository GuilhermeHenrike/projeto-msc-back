from flask import redirect, request, session, jsonify, render_template

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

        if publicacao == "BLOQUEADO":
            return jsonify({
                "error": "A publicação foi bloqueada pela moderação."
            }), 400

        if publicacao == "ERRO":
            return jsonify({
                "error": "Erro ao salvar a publicação."
            }), 500

        return jsonify({
            "message": "Publicação criada com sucesso."
        }), 201


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

    @app.route("/publicacoes", methods=["GET"])
    def carregarPublicacoes():

        publicacoes = publicacaoService.carregarPublicacao()

        return jsonify(publicacoes), 200