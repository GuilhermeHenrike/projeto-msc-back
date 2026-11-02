from flask import redirect, request, session, jsonify


def comentarioController(app, comentarioService, notificacaoService):

    # Listar comentários de uma publicação
    @app.route("/comentarios/<int:publicacao_id>")
    def comentarios(publicacao_id):

        if "user.id" not in session:
            return redirect("/")

        comentarios = comentarioService.carregarComentarios(publicacao_id)

        usuario_id = session["user.id"]

        for comentario in comentarios:
            comentario["eh_dono"] = (
                comentario["usuario_id"] == usuario_id
            )

        return jsonify(comentarios)

    # Criar comentário
    @app.route("/comentario", methods=["POST"])
    def criarComentario():

        if "user.id" not in session:
            return jsonify({"erro": "Não autenticado"}), 401

        dados = request.get_json()

        texto = dados.get("texto")
        publicacao_id = dados.get("publicacao_id")

        if not texto:
            return jsonify({"erro": "Digite um comentário"}), 400

        if not publicacao_id:
            return jsonify({"erro": "Publicação não informada"}), 400

        usuario_id = session["user.id"]

        comentarioService.criarComentario(
            texto,
            usuario_id,
            publicacao_id
        )

        # Criar notificação para o autor da publicação
        notificacaoService.notificarInteracao(
            usuario_origem_id=usuario_id,
            publicacao_id=publicacao_id,
            tipo="comentario"
        )

        return jsonify("Comentário criado"), 201

    # Editar comentário
    @app.route("/comentario/<int:id>", methods=["PUT"])
    def editarComentario(id):

        if "user.id" not in session:
            return redirect("/")

        dados = request.get_json()
        texto = dados.get("texto")

        if not texto:
            return "Digite um comentário"

        usuario_id = session["user.id"]

        comentarioService.editarComentario(id, usuario_id, texto)

        return jsonify("Comentário editado")

    # Apagar comentário
    @app.route("/comentario/<int:id>", methods=["DELETE"])
    def apagarComentario(id):

        if "user.id" not in session:
            return redirect("/")

        usuario_id = session["user.id"]

        comentarioService.apagarComentario(id, usuario_id)

        return jsonify("Comentário apagado")