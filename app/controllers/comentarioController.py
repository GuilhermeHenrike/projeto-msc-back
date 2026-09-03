from flask import redirect, request, session, render_template


def comentarioController(app, comentarioService):


    @app.route("/comentarios/<int:publicacao_id>")
    def comentarios(publicacao_id):

        if "user.id" not in session:
            return redirect("/")

        comentarios = comentarioService.carregarComentarios(publicacao_id)

        return render_template(
            "Comentarios.html",
            comentarios=comentarios,
            publicacao_id=publicacao_id
        )


    @app.route("/comentario", methods=["POST"])
    def criarComentario():

        if "user.id" not in session:
            return redirect("/")

        texto = request.form.get("texto")
        publicacao_id = request.form.get("publicacao_id")

        if not texto:
            return "Digite um comentário"

        if not publicacao_id:
            return "Publicação não informada"

        usuario_id = session["user.id"]

        comentario = comentarioService.criarComentario(
            texto,
            usuario_id,
            publicacao_id
        )

        if comentario is None:
            return render_template(
                "Comentarios.html",
                comentarios=comentarioService.carregarComentarios(publicacao_id),
                publicacao_id=publicacao_id,
                mensagem="Comentário bloqueado pela moderação."
    )

        return redirect(f"/comentarios/{publicacao_id}")


    @app.route("/comentario/<int:id>", methods=["PUT"])
    def editarComentario(id):

        if "user.id" not in session:
            return redirect("/")

        texto = request.form.get("texto")

        if not texto:
            return "Digite um comentário"

        usuario_id = session["user.id"]

        comentarioService.editarComentario(
            id,
            usuario_id,
            texto
        )

        return "Comentário editado"


    @app.route("/comentario/<int:id>", methods=["DELETE"])
    def apagarComentario(id):

        if "user.id" not in session:
            return redirect("/")

        usuario_id = session["user.id"]

        comentarioService.apagarComentario(
            id,
            usuario_id
        )

        return "Comentário apagado"