from flask import redirect, request, session, jsonify

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


    @app.route("/perfil/<int:usuario_id>", methods=["GET"])
    def buscarPerfil(usuario_id):

        perfil = perfilService.buscarPerfil(usuario_id)

        if perfil is None:
            return jsonify({
                "error": "Usuário não encontrado."
            }), 404

        return jsonify(perfil), 200