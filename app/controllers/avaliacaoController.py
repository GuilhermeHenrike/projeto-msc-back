from flask import request, session, jsonify


def avaliacaoController(app, avaliacaoService):


    @app.route("/avaliacoes", methods=["POST"])
    def salvarAvaliacao():

        if "user.id" not in session:
            return jsonify({"erro": "Usuário não está logado."}), 401

        usuario_id = session["user.id"]
        dados = request.get_json(silent=True) or {}
        album_id = dados.get("album_id")
        nota = dados.get("nota")

        if album_id is None or nota is None:
            return jsonify({"erro": "Informe o álbum e a nota."}), 400

        try:
            avaliacao = avaliacaoService.salvarAvaliacao(usuario_id, album_id, nota)

            return jsonify({
                "mensagem": "Avaliação criada com sucesso!",
                "avaliacao": {
                    "album_id": avaliacao.album_id,
                    "nota": avaliacao.nota
                }
            }), 201

        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400


    @app.route("/avaliacoes/<int:album_id>", methods=["PUT"])
    def editarAvaliacao(album_id):

        if "user.id" not in session:
            return jsonify({"erro": "Usuário não está logado."}), 401

        usuario_id = session["user.id"]
        dados = request.get_json(silent=True) or {}
        nota = dados.get("nota")

        if nota is None:
            return jsonify({"erro": "Informe a nova nota."}), 400

        try:
            avaliacao = avaliacaoService.editarAvaliacao(usuario_id, album_id, nota)

            return jsonify({
                "mensagem": "Avaliação atualizada com sucesso!",
                "avaliacao": {
                    "album_id": avaliacao["album_id"],
                    "nota": avaliacao["nota"]
                }
            }), 200

        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400


    @app.route("/avaliacoes", methods=["GET"])
    def carregarAvaliacoes():

        if "user.id" not in session:
            return jsonify({"erro": "Usuário não está logado."}), 401

        usuario_id = session["user.id"]
        avaliacoes = avaliacaoService.carregarAvaliacoesUsuario(usuario_id)

        return jsonify(avaliacoes), 200