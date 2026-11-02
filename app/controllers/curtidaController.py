
from flask import jsonify, session
import logging

logger = logging.getLogger(__name__)


def curtidaController(app, curtidaService, notificacaoService):

    @app.route("/curtir/<int:publicacao_id>", methods=["POST"])
    def curtir(publicacao_id):

        if "user.id" not in session:
            return jsonify({"erro": "Não autenticado"}), 401

        usuario_id = session["user.id"]

        try:
            curtido = curtidaService.curtir(
                usuario_id,
                publicacao_id
            )

            # Criar notificação somente quando a curtida é adicionada
            if curtido:
                try:
                    notificacaoService.notificarInteracao(
                        usuario_origem_id=usuario_id,
                        publicacao_id=publicacao_id,
                        tipo="curtida"
                    )

                except Exception:
                    logger.exception(
                        "Erro ao criar notificação de curtida"
                    )

            total_curtidas = curtidaService.contarCurtidas(
                publicacao_id
            )

            return jsonify({
                "curtido": curtido,
                "total_curtidas": total_curtidas
            }), 200

        except Exception:
            logger.exception(
                "Erro ao curtir ou descurtir publicação"
            )

            return jsonify({
                "erro": "Erro ao curtir a publicação"
            }), 500
