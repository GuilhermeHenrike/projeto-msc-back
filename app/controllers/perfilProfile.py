from flask import redirect, request, session, jsonify

def perfilController(app, perfilService):

    @app.route("/perfil", methods=["GET"])
    def buscarPerfil():

        if "user.id" not in session:
            return jsonify({"erro": "Usuário não autenticado"}), 401

        usuario_id = session["user.id"]

        usuario = perfilService.buscarPerfil(usuario_id)

        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        return jsonify(usuario), 200


    @app.route("/perfil", methods=["POST"])
    def editarPerfil():

        if "user.id" not in session:
            return redirect("/")

        nome = request.form.get("nome")
        foto_url = request.form.get("foto_url")

        usuario_id = session["user.id"]

        perfilService.atualizarPerfil(nome, foto_url, usuario_id)

        return redirect("/home")