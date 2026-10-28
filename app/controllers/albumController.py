from flask import request, session, jsonify


def albumController(app, albumService):


    @app.route("/albuns/buscar", methods=["GET"])
    def buscarAlbuns():

        if "user.id" not in session:
            return jsonify({"erro": "Usuário não está logado."}), 401

        query = request.args.get("query", "").strip()

        if not query:
            return jsonify({"erro": "Informe o nome do álbum."}), 400

        try:
            albuns = albumService.buscarAlbunsDeezer(query)
            return jsonify(albuns), 200
        except RuntimeError as erro:
            return jsonify({"erro": str(erro)}), 502


    @app.route("/albuns/salvar", methods=["POST"])
    def salvarAlbum():

        if "user.id" not in session:
            return jsonify({"erro": "Usuário não está logado."}), 401

        usuario_id = session["user.id"]
        dados = request.get_json(silent=True) or {}
        campos_obrigatorios = ["deezer_id", "titulo", "artista", "capa_url"]

        for campo in campos_obrigatorios:
            if campo not in dados:
                return jsonify({"erro": "Dados do álbum incompletos."}), 400

        try:
            album = albumService.salvarAlbumUsuario(usuario_id, dados)

            if isinstance(album, dict):
                album_resposta = album
            else:
                album_resposta = {
                    "id": album.id,
                    "deezer_id": album.deezer_id,
                    "titulo": album.titulo,
                    "artista": album.artista,
                    "capa_url": album.capa_url
                }

            return jsonify({
                "mensagem": "Álbum salvo com sucesso!",
                "album": album_resposta
            }), 201

        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400


    @app.route("/albuns/salvos", methods=["GET"])
    def carregarAlbunsSalvos():

        if "user.id" not in session:
            return jsonify({"erro": "Usuário não está logado."}), 401

        usuario_id = session["user.id"]

        albuns = albumService.carregarAlbunsSalvos(usuario_id)
        return jsonify(albuns), 200


    @app.route("/albuns/salvos/<int:album_id>", methods=["DELETE"])
    def removerAlbumSalvo(album_id):

        if "user.id" not in session:
            return jsonify({"erro": "Usuário não está logado."}), 401

        usuario_id = session["user.id"]

        albumService.removerAlbumUsuario(usuario_id, album_id)
        return "", 204