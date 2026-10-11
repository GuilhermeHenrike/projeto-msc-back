from flask import request, session, jsonify


def perfilController(app, perfilService):

    @app.route("/perfil", methods=["POST"])
    def editarPerfil():

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401
        
        nome = request.form.get("nome")
        foto_url = request.form.get("foto_url")
        usuario_id = session["user.id"]

        perfilService.atualizarPerfil(nome, foto_url, usuario_id)

        return {"mensagem": "Perfil atualizado com sucesso"}, 200


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
            "foto_url": usuario["foto_url"]
        }, 200