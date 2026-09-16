from flask import redirect, request, session, render_template, jsonify


def comentarioController(app, comentarioService):


    @app.route("/comentarios/<int:publicacao_id>")
    def comentarios(publicacao_id):

        if "user.id" not in session:
            return redirect("/")

        comentarios = comentarioService.carregarComentarios(publicacao_id)

        return jsonify(comentarios)


    @app.route("/comentario", methods=["POST"])
    def criarComentario():

        if "user.id" not in session:
            return redirect("/")

        dados = request.get_json()

        texto = dados.get("texto")
        publicacao_id = dados.get("publicacao_id")

        if not texto:
            return "Digite um comentário"

        if not publicacao_id:
            return "Publicação não informada"

        usuario_id = session["user.id"]

        comentarioService.criarComentario( texto, usuario_id, publicacao_id)

        return jsonify("Comentário criado")


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


    @app.route("/comentario/<int:id>", methods=["DELETE"])
    def apagarComentario(id):

        if "user.id" not in session:
            return redirect("/")

        usuario_id = session["user.id"]

        comentarioService.apagarComentario(id, usuario_id)
        return jsonify("Comentário apagado")