from flask import redirect, request, session

def perfilController(app, perfilService):

    @app.route("/perfil", methods=["POST"])
    def editarPerfil():

        if "user.id" not in session:
            return redirect("/")

        nome = request.form.get("nome")
        foto_url = request.form.get("foto_url")

        usuario_id = session["user.id"]

        perfilService.atualizarPerfil(nome, foto_url, usuario_id)

        return redirect("/home")