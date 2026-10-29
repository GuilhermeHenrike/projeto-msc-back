from flask import jsonify, session

def curtidaController(app, curtidaService):

    @app.route("/curtir/<int:publicacao_id>", methods=["POST"])
    def curtir(publicacao_id):

        if "user.id" not in session:
            return jsonify({"erro": "Não autenticado"}), 401

        usuario_id = session["user.id"]

        curtido = curtidaService.curtir(
            usuario_id,
            publicacao_id
        )

        total_curtidas = curtidaService.contarCurtidas(
            publicacao_id
        )

        return jsonify({
            "curtido": curtido,
            "total_curtidas": total_curtidas
        }), 200