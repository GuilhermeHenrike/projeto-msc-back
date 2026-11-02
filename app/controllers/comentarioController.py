
from flask import redirect, request, session, jsonify
import logging

logger = logging.getLogger(__name__)


def comentarioController(app, comentarioService, notificacaoService):

    # =========================
    # LISTAR COMENTÁRIOS
    # =========================

    @app.route("/comentarios/<int:publicacao_id>")
    def comentarios(publicacao_id):

        if "user.id" not in session:
            return jsonify({"erro": "Não autenticado"}), 401

        comentarios = comentarioService.carregarComentarios(
            publicacao_id
        )

        usuario_id = session["user.id"]

        for comentario in comentarios:
            comentario["eh_dono"] = (
                comentario["usuario_id"] == usuario_id
            )

        return jsonify(comentarios), 200

    # =========================
    # CRIAR COMENTÁRIO
    # =========================

    @app.route("/comentario", methods=["POST"])
    def criarComentario():

        if "user.id" not in session:
            return jsonify({"erro": "Não autenticado"}), 401

        dados = request.get_json()

        if not dados:
            return jsonify({
                "erro": "Dados não informados"
            }), 400

        texto = dados.get("texto")
        publicacao_id = dados.get("publicacao_id")

        if not texto or not texto.strip():
            return jsonify({
                "erro": "Digite um comentário"
            }), 400

        if not publicacao_id:
            return jsonify({
                "erro": "Publicação não informada"
            }), 400

        usuario_id = session["user.id"]

        try:
            comentarioService.criarComentario(
                texto,
                usuario_id,
                publicacao_id
            )

            # Criar notificação sem impedir o comentário
            try:
                notificacaoService.notificarInteracao(
                    usuario_origem_id=usuario_id,
                    publicacao_id=publicacao_id,
                    tipo="comentario"
                )

            except Exception:
                logger.exception(
                    "Erro ao criar notificação de comentário"
                )

            return jsonify({
                "mensagem": "Comentário criado"
            }), 201

        except Exception:
            logger.exception(
                "Erro ao criar comentário"
            )

            return jsonify({
                "erro": "Erro ao criar comentário"
            }), 500

    # =========================
    # EDITAR COMENTÁRIO
    # =========================

    @app.route("/comentario/<int:id>", methods=["PUT"])
    def editarComentario(id):

        if "user.id" not in session:
            return jsonify({
                "erro": "Não autenticado"
            }), 401

        dados = request.get_json()

        if not dados:
            return jsonify({
                "erro": "Dados não informados"
            }), 400

        texto = dados.get("texto")

        if not texto or not texto.strip():
            return jsonify({
                "erro": "Digite um comentário"
            }), 400

        usuario_id = session["user.id"]

        try:
            comentarioService.editarComentario(
                id,
                usuario_id,
                texto
            )

            return jsonify({
                "mensagem": "Comentário editado"
            }), 200

        except Exception:
            logger.exception(
                "Erro ao editar comentário"
            )

            return jsonify({
                "erro": "Erro ao editar comentário"
            }), 500

    # =========================
    # APAGAR COMENTÁRIO
    # =========================

    @app.route("/comentario/<int:id>", methods=["DELETE"])
    def apagarComentario(id):

        if "user.id" not in session:
            return jsonify({
                "erro": "Não autenticado"
            }), 401

        usuario_id = session["user.id"]

        try:
            comentarioService.apagarComentario(
                id,
                usuario_id
            )

            return jsonify({
                "mensagem": "Comentário apagado"
            }), 200

        except Exception:
            logger.exception(
                "Erro ao apagar comentário"
            )

            return jsonify({
                "erro": "Erro ao apagar comentário"
            }), 500
