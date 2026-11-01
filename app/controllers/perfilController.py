from flask import request, session, jsonify


def perfilController(app, perfilService):

    @app.route("/perfil", methods=["POST"])
    def editarPerfil():
        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        nome = request.form.get("nome", "").strip()
        usuario_id = session["user.id"]

        if not nome:
            return {"erro": "O nome não pode ficar vazio."}, 400

        foto_perfil = request.files.get("foto_perfil")
        foto_capa = request.files.get("foto_url_background")

        try:
            perfilService.atualizarPerfil(
                nome=nome,
                usuario_id=usuario_id,
                foto_perfil=foto_perfil,
                foto_url_background=foto_capa
            )

            return {
                "mensagem": "Perfil atualizado com sucesso"
            }, 200

        except Exception as erro:
            print(f"Erro ao atualizar perfil: {erro}")
            return {
                "erro": "Não foi possível atualizar o perfil."
            }, 500



    @app.route("/perfil/<int:usuario_id>", methods=["GET"])
    def buscarPerfil(usuario_id):

        perfil = perfilService.buscarPerfilComDados(usuario_id)

        if perfil is None:
            return jsonify({
                "error": "Usuário não encontrado."
            }), 404

        return jsonify(perfil), 200


    @app.route("/perfil", methods=["GET"])
    def perfil():

        usuario_id = session.get("user.id")

        if not usuario_id:
            return {"erro": "Usuário não está logado"}, 401

        usuario = perfilService.buscarPerfil(usuario_id)

        if not usuario:
            return {"erro": "Usuário não encontrado"}, 404

        return {
            "id": usuario["id"],
            "nome": usuario["nome"],
            "email": usuario["email"],
            "foto_url": usuario["foto_url"],
            "foto_url_background": usuario["foto_url_background"]
        }, 200


    @app.route("/buscarUsuarios", methods=["GET"])
    def buscarUsuarios():

        if "user.id" not in session:
            return jsonify({"erro": "Não autenticado"}), 401

        nome = request.args.get("nome", "").strip()

        if not nome:
            return jsonify([]), 200

        usuario_id = session["user.id"]

        usuarios = perfilService.buscarUsuariosPorNome(nome, usuario_id)

        return jsonify(usuarios), 200