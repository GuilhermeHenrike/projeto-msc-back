from flask import redirect, session


def curtidaController(app, curtidaService):

    @app.route("/curtir/<int:publicacao_id>", methods=["POST"])
    def curtir(publicacao_id):

        if "user.id" not in session:
            return redirect("/")

        usuario_id = session["user.id"]

        curtidaService.curtir(usuario_id, publicacao_id)

        return redirect("/home")