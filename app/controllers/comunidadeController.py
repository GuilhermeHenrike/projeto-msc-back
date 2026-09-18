from flask import request, session
from mysql.connector.errors import IntegrityError
import cloudinary.uploader
from flask import redirect, request, session, jsonify

def comunidadeController(app, comunidadeService):

    @app.route("/comunidade", methods=["POST"])
    def criarComunidade():

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        nome = request.form.get("nome")
        genero = request.form.get("genero")
        descricao = request.form.get("descricao")
        imagem_frontend = request.files.get("imagem_url") ## pega a imagem do front
        imagem_url = None ## nulo pq nao sabe se o usuario mandou ou nao imagem

        if imagem_frontend: ## se tiver imagem ele da upload e seta como imagem_url
            resultado = cloudinary.uploader.upload(imagem_frontend)
            imagem_url = resultado["secure_url"]

        usuario_id = session["user.id"]

        try:
            comunidadeService.criarComunidade(nome, genero, usuario_id, descricao, imagem_url)
            return {"mensagem": "Comunidade criada com sucesso"}, 201
    
        except IntegrityError:
            return {"erro": "Já existe uma comunidade com esse nome"}, 409


    @app.route("/comunidade/<int:id>", methods=["PUT"])
    def atualizarComunidade(id):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        comunidade = comunidadeService.listarComunidade(id)

        if comunidade is None:
            return {"erro": "Comunidade não encontrada"}, 404

        if session["user.id"] != comunidade["criador_id"]:
            return {"erro": "Não autorizado"}, 403
        
        nome = request.form.get("nome")
        genero = request.form.get("genero")
        descricao = request.form.get("descricao")
        imagem_url = request.form.get("imagem_url")
        nova_imagem = request.files.get("imagem")

        if nova_imagem: ## se ele mandou outra imagem então troca imagem_url pela nova imagem
            resultado = cloudinary.uploader.upload(nova_imagem)
            imagem_url = resultado["secure_url"]

        comunidadeService.atualizarComunidade(nome, genero, descricao, imagem_url, id)
        return {"mensagem": "Comunidade atualizada com sucesso"}, 200


    @app.route("/comunidade/<int:id>", methods=["DELETE"])
    def apagarComunidade(id):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        comunidade = comunidadeService.listarComunidade(id)

        if comunidade is None:
            return {"erro": "Comunidade não encontrada"}, 404
        
        if session["user.id"] != comunidade["criador_id"]:
            return {"erro": "Não autorizado"}, 403

        comunidadeService.apagarComunidade(id)

        return "", 204


    ## ROTAS DE BUSCA

    @app.route("/buscarComunidadesDisponiveis", methods=["GET"])
    def buscarComunidadesDisponiveis():

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401


        usuario_id = session["user.id"]

        return comunidadeService.listarComunidadesNaoParticipa(usuario_id)


    @app.route("/buscarComunidade/<int:comunidade_id>", methods=["GET"])
    def buscarComunidade(comunidade_id):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401


        comunidade = comunidadeService.listarComunidade(comunidade_id)

        if comunidade is None:
            return {"erro": "Comunidade não encontrada"}, 404
        
        return comunidade


    @app.route("/buscarComunidadeUsuario", methods=["GET"])
    def buscarComunidadeUsuario():

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401


        usuario_id = session["user.id"]

        return comunidadeService.listarTodasComunidadesDoUsuario(usuario_id)

    
    ## FILTRO

    @app.route("/filtroGeneroComunidade/<string:genero>", methods=["GET"])
    def filtroGeneroComunidade(genero):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401


        return comunidadeService.filtroComunidadesPorGenero(genero)


    ## ENTRAR E SAIR DAS COMUNIDADES


    @app.route("/entrarComunidade/<int:comunidade_id>", methods=["POST"])
    def entrarComunidade(comunidade_id):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401


        usuario_id = session["user.id"]

        comunidadeService.entrarComunidade(usuario_id, comunidade_id)

        return {"mensagem": "Entrou na comunidade com sucesso"}, 200


    @app.route("/sairComunidade/<int:comunidade_id>", methods=["POST"])
    def sairComunidade(comunidade_id):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401


        usuario_id = session["user.id"]

        comunidadeService.sairComunidade(usuario_id, comunidade_id)

        return {"mensagem": "Saiu da comunidade com sucesso"}, 200