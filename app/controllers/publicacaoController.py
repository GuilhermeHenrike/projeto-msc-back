
from flask import request, session, jsonify


def publicacaoController(app, publicacaoService):

    # CRIAR PUBLICAÇÃO
    @app.route("/publicacao", methods=["POST"])
    def criarPublicacao():

        if "user.id" not in session:
            return jsonify({
                "error": "Você precisa estar logado."
            }), 401

        arquivo = request.files.get("imagem")
        legenda = request.form.get("legenda", "").strip()
        comunidade_id = request.form.get("comunidade")

        if arquivo is None or not arquivo.filename:
            return jsonify({
                "error": "Selecione uma imagem ou um vídeo."
            }), 400

        tipo_mime = arquivo.mimetype or ""

        if tipo_mime.startswith("image/"):
            tipo_midia = "imagem"
        elif tipo_mime.startswith("video/"):
            tipo_midia = "video"
        else:
            return jsonify({
                "error": "Formato de arquivo não permitido."
            }), 400

        if not comunidade_id:
            return jsonify({
                "error": "Selecione uma comunidade."
            }), 400

        usuario_id = session["user.id"]

        publicacao = publicacaoService.criarPublicacao(
            arquivo,
            legenda,
            usuario_id,
            comunidade_id,
            tipo_midia
        )

        if publicacao == "BLOQUEADO":
            return jsonify({
                "error": (
                    "A imagem, o vídeo ou a legenda contém "
                    "conteúdo não permitido."
                )
            }), 422

        if publicacao == "DADOS_INVALIDOS":
            return jsonify({
                "error": (
                    "O arquivo está vazio, é inválido "
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

        if publicacao == "NAO_PARTICIPA":
            return jsonify({
                "error": (
                    "Você precisa participar da comunidade "
                    "para publicar."
                )
            }), 403

        if publicacao == "ERRO":
            return jsonify({
                "error": "Erro ao salvar a publicação."
            }), 500

        return jsonify({
            "message": "Publicação criada com sucesso."
        }), 201

    # APAGAR PUBLICAÇÃO
    @app.route("/apagar-publicacao/<int:id>", methods=["DELETE"])
    def apagarPublicacao(id):

        if "user.id" not in session:
            return jsonify({
                "error": "Usuário não está logado."
            }), 401

        usuario_id = int(session["user.id"])

        publicacao = publicacaoService.buscarPublicacao(id)

        if publicacao is None:
            return jsonify({
                "error": "Publicação não encontrada."
            }), 404

        comunidade = publicacaoService.buscarComunidade(
            publicacao["comunidade_id"]
        )

        if comunidade is None:
            return jsonify({
                "error": "Comunidade não encontrada."
            }), 404

        eh_autor = (
            usuario_id == int(publicacao["usuario_id"])
        )

        eh_criador = (
            usuario_id == int(comunidade["criador_id"])
        )

        if not (eh_autor or eh_criador):
            return jsonify({
                "error": (
                    "Você não tem permissão para "
                    "apagar esta publicação."
                )
            }), 403

        publicacaoService.apagarPublicacao(id)

        return "", 204

    # FEED DESCOBRIR
    @app.route("/publicacoes", methods=["GET"])
    def carregarPublicacoes():

        usuario_id = session.get("user.id")

        # Passa o usuário para verificar suas curtidas
        publicacoes = publicacaoService.carregarPublicacao(
            usuario_id
        )

        for publicacao in publicacoes:
            publicacao["eh_dono"] = (
                int(publicacao["usuario_id"]) == int(usuario_id)
                if usuario_id is not None
                else False
            )

        return jsonify(publicacoes), 200

    # PUBLICAÇÕES DE UMA COMUNIDADE
    @app.route(
        "/publicacoes/comunidade/<int:comunidade_id>",
        methods=["GET"]
    )
    def carregarPublicacoesComunidade(comunidade_id):

        usuario_id = session.get("user.id")

        # Passa o usuário para verificar suas curtidas
        publicacoes = (
            publicacaoService.carregarPublicacoesPorComunidade(
                comunidade_id,
                usuario_id
            )
        )

        for publicacao in publicacoes:
            publicacao["eh_dono"] = (
                int(publicacao["usuario_id"]) == int(usuario_id)
                if usuario_id is not None
                else False
            )

        return jsonify(publicacoes), 200

    # FEED SEGUINDO
    @app.route("/publicacoes/seguindo", methods=["GET"])
    def publicacoesSeguindo():

        usuario_id = session.get("user.id")

        if not usuario_id:
            return jsonify({
                "erro": "Usuário não autenticado"
            }), 401

        try:
            publicacoes = (
                publicacaoService.listarFeedSeguindo(
                    usuario_id
                )
            )

            return jsonify(publicacoes), 200

        except Exception as erro:
            print(
                "Erro ao buscar publicações das "
                f"comunidades seguidas: {erro}"
            )

            return jsonify({
                "erro": (
                    "Não foi possível carregar as publicações "
                    "das comunidades seguidas."
                )
            }), 500
