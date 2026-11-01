
from flask import jsonify


def artistasController(app, artistasService):

    @app.route("/artistas-em-alta", methods=["GET"])
    def listarArtistasEmAlta():

        try:
            artistas = artistasService.listarArtistasEmAlta()

            return jsonify({
                "sucesso": True,
                "artistas": artistas
            }), 200

        except RuntimeError as erro:
            app.logger.error(
                "Erro ao consultar artistas na Deezer: %s",
                erro
            )

            return jsonify({
                "sucesso": False,
                "erro": "Não foi possível carregar os artistas da Deezer."
            }), 502

        except Exception:
            app.logger.exception(
                "Erro inesperado ao carregar artistas."
            )

            return jsonify({
                "sucesso": False,
                "erro": "Ocorreu um erro interno no servidor."
            }), 500
