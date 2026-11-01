from flask import jsonify, session


def notificacaoController(app, notificacaoService):

    @app.route("/notificacoes", methods=["GET"])
    def listarNotificacoes():

        if "user.id" not in session:
            return jsonify({"erro": "Não autenticado"}), 401

        usuario_id = session["user.id"]

        notificacoes = notificacaoService.listarNotificacoes(usuario_id)

        return jsonify(notificacoes), 200