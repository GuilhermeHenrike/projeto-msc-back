
from flask import request, session, jsonify


def publicacaoController(app, publicacaoService):

    @app.route("/publicacao", methods=["POST"])
    def criarPublicacao():

        if "user.id" not in session:
            return jsonify({
                "error": "Você precisa estar logado."
            }), 401

        imagem = request.files.get("imagem")
        legenda = request.form.get("legenda", "").strip()
        comunidade_id = request.form.get("comunidade")

        if imagem is None or not imagem.filename:
            return jsonify({
                "error": "Selecione uma imagem."
            }), 400

        if not comunidade_id:
            return jsonify({
                "error": "Selecione uma comunidade."
            }), 400

        usuario_id = session["user.id"]

        publicacao = publicacaoService.criarPublicacao(
            imagem,
            legenda,
            usuario_id,
            comunidade_id
        )

        if publicacao == "BLOQUEADO":
            return jsonify({
                "error": (
                    "A imagem ou legenda contém "
                    "conteúdo não permitido."
                )
            }), 422

        if publicacao == "DADOS_INVALIDOS":
            return jsonify({
                "error": (
                    "A imagem está vazia, é inválida "
                    "ou seu formato não é suportado."
                )
            }), 400

        if publicacao == "ERRO_MODERACAO":
            return jsonify({
                "error": (
                    "Não foi possível verificar o conteúdo "
                    "agora. Tente novamente."
                )
            }), 503

        if publicacao == "ERRO":
            return jsonify({
                "error": "Erro ao salvar a publicação."
            }), 500

        return jsonify({
            "message": "Publicação criada com sucesso."
        }), 201

    @app.route(
        "/apagar-publicacao/<int:id>",
        methods=["DELETE"]
    )
    def apagarPublicacao(id):

        if "user.id" not in session:
            return jsonify({
                "error": "Usuário não está logado."
            }), 401

        publicacao = publicacaoService.buscarPublicacao(id)

        if publicacao is None:
            return jsonify({
                "error": "Publicação não encontrada."
            }), 404

        if publicacao["usuario_id"] != session["user.id"]:
            return jsonify({
                "error": "Você não pode apagar essa publicação."
            }), 403

        publicacaoService.apagarPublicacao(id)

        return "", 204

    @app.route("/publicacoes", methods=["GET"])
    def carregarPublicacoes():

        publicacoes = publicacaoService.carregarPublicacao()
        usuario_id = session.get("user.id")

        for publicacao in publicacoes:
            publicacao["eh_dono"] = (
                publicacao["usuario_id"] == usuario_id
            )

        return jsonify(publicacoes), 200

    @app.route(
        "/publicacoes/comunidade/<int:comunidade_id>",
        methods=["GET"]
    )
    def carregarPublicacoesComunidade(comunidade_id):

        publicacoes = (
            publicacaoService.carregarPublicacoesPorComunidade(
                comunidade_id
            )
        )

        usuario_id = session.get("user.id")

        for publicacao in publicacoes:
            publicacao["eh_dono"] = (
                publicacao["usuario_id"] == usuario_id
            )

        return jsonify(publicacoes), 200
