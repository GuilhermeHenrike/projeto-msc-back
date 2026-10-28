from flask import request, session, jsonify


def composicaoController(app, composicaoService):

    @app.route("/composicoes", methods=["POST"])
    def criarComposicao():
        if "user.id" not in session:
            return jsonify({
                "erro": "Usuário não está logado."
            }), 401

        dados = request.get_json(silent=True)

        if not isinstance(dados, dict):
            return jsonify({
                "erro": "Envie os dados da composição."
            }), 400

        try:
            composicao = composicaoService.criar(
                session["user.id"],
                dados
            )

            return jsonify({
                "mensagem": "Composição salva com sucesso!",
                "composicao": composicao
            }), 201

        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

        except Exception:
            app.logger.exception("Erro ao criar composição")

            return jsonify({
                "erro": "Não foi possível salvar a composição."
            }), 500

    @app.route("/composicoes", methods=["GET"])
    def listarComposicoes():
        if "user.id" not in session:
            return jsonify({
                "erro": "Usuário não está logado."
            }), 401

        try:
            composicoes = composicaoService.listar(
                session["user.id"]
            )

            return jsonify(composicoes), 200

        except Exception:
            app.logger.exception("Erro ao listar composições")

            return jsonify({
                "erro": "Não foi possível carregar as composições."
            }), 500

    @app.route("/composicoes/<int:id>", methods=["GET"])
    def buscarComposicao(id):
        if "user.id" not in session:
            return jsonify({
                "erro": "Usuário não está logado."
            }), 401

        try:
            composicao = composicaoService.buscar(
                id,
                session["user.id"]
            )

            if not composicao:
                return jsonify({
                    "erro": "Composição não encontrada."
                }), 404

            return jsonify(composicao), 200

        except Exception:
            app.logger.exception("Erro ao buscar composição")

            return jsonify({
                "erro": "Não foi possível buscar a composição."
            }), 500

    @app.route("/composicoes/<int:id>", methods=["PUT"])
    def atualizarComposicao(id):
        if "user.id" not in session:
            return jsonify({
                "erro": "Usuário não está logado."
            }), 401

        dados = request.get_json(silent=True)

        if not isinstance(dados, dict):
            return jsonify({
                "erro": "Envie os dados da composição."
            }), 400

        try:
            composicao = composicaoService.atualizar(
                id,
                session["user.id"],
                dados
            )

            if composicao is None:
                return jsonify({
                    "erro": "Composição não encontrada."
                }), 404

            return jsonify({
                "mensagem": "Composição atualizada com sucesso!",
                "composicao": composicao
            }), 200

        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

        except Exception:
            app.logger.exception("Erro ao atualizar composição")

            return jsonify({
                "erro": "Não foi possível atualizar a composição."
            }), 500

    @app.route("/composicoes/<int:id>", methods=["DELETE"])
    def excluirComposicao(id):
        if "user.id" not in session:
            return jsonify({
                "erro": "Usuário não está logado."
            }), 401

        try:
            excluida = composicaoService.excluir(
                id,
                session["user.id"]
            )

            if not excluida:
                return jsonify({
                    "erro": "Composição não encontrada."
                }), 404

            return "", 204

        except Exception:
            app.logger.exception("Erro ao excluir composição")

            return jsonify({
                "erro": "Não foi possível excluir a composição."
            }), 500

            
    @app.route("/composicoes/publicas", methods=["GET"])
    def listarComposicoesPublicas():
        try:
            composicoes = composicaoService.listarPublicas()
            return jsonify(composicoes), 200

        except Exception:
            app.logger.exception("Erro ao listar letras públicas")

            return jsonify({
                "erro": "Não foi possível carregar as letras públicas."
            }), 500

    @app.route("/composicoes/publicas/<int:id>", methods=["GET"])
    def buscarComposicaoPublica(id):
        try:
            composicao = composicaoService.buscarPublica(id)

            if not composicao:
                return jsonify({
                    "erro": "Composição pública não encontrada."
                }), 404

            return jsonify(composicao), 200

        except Exception:
            app.logger.exception("Erro ao buscar letra pública")

            return jsonify({
                "erro": "Não foi possível carregar a letra."
            }), 500


            