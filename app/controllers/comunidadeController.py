
from flask import request, session
import cloudinary.uploader


def comunidadeController(app, comunidadeService):

    # CRIAR COMUNIDADE

    @app.route("/comunidade", methods=["POST"])
    def criarComunidade():

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        nome = request.form.get("nome")
        genero = request.form.get("genero")
        descricao = request.form.get("descricao")
        imagem_frontend = request.files.get("imagem_url")
        imagem_url = None

        if imagem_frontend:
            resultado = cloudinary.uploader.upload(imagem_frontend)
            imagem_url = resultado["secure_url"]

        usuario_id = session["user.id"]

        comunidadeService.criarComunidade(
            nome, genero, usuario_id, descricao, imagem_url
        )

        return {"mensagem": "Comunidade criada com sucesso"}, 201


    # ATUALIZAR COMUNIDADE

    @app.route("/comunidade/<int:id>", methods=["PUT"])
    def atualizarComunidade(id):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        comunidade = comunidadeService.listarComunidade(id)

        if comunidade is None:
            return {"erro": "Comunidade não encontrada"}, 404

        if int(session["user.id"]) != int(comunidade["criador_id"]):
            return {"erro": "Não autorizado"}, 403

        nome = request.form.get("nome")
        genero = request.form.get("genero")
        descricao = request.form.get("descricao")
        imagem_url = request.form.get("imagem_url")
        nova_imagem = request.files.get("imagem")

        if nova_imagem:
            resultado = cloudinary.uploader.upload(nova_imagem)
            imagem_url = resultado["secure_url"]

        comunidadeService.atualizarComunidade(
            nome, genero, descricao, imagem_url, id
        )

        return {"mensagem": "Comunidade atualizada com sucesso"}, 200


    # APAGAR COMUNIDADE

    @app.route("/comunidade/<int:id>", methods=["DELETE"])
    def apagarComunidade(id):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        comunidade = comunidadeService.listarComunidade(id)

        if comunidade is None:
            return {"erro": "Comunidade não encontrada"}, 404

        if int(session["user.id"]) != int(comunidade["criador_id"]):
            return {"erro": "Não autorizado"}, 403

        comunidadeService.apagarComunidade(id)

        return "", 204


    # COMUNIDADES DISPONÍVEIS

    @app.route("/buscarComunidadesDisponiveis", methods=["GET"])
    def buscarComunidadesDisponiveis():

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        usuario_id = session["user.id"]

        return comunidadeService.listarComunidadesNaoParticipa(usuario_id)


    # COMUNIDADES QUE O USUARIO É DONO
    
    @app.route("/minhasComunidades", methods=["GET"])
    def minhasComunidades():

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        usuario_id = session["user.id"]

        comunidades = comunidadeService.listarComunidadesDoCriador(usuario_id)

        return comunidades


    # BUSCAR UMA COMUNIDADE PELO ID

    @app.route("/buscarComunidade/<int:comunidade_id>", methods=["GET"])
    def buscarComunidade(comunidade_id):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        usuario_id = session["user.id"]

        comunidade = comunidadeService.listarComunidade(comunidade_id)

        if comunidade is None:
            return {"erro": "Comunidade não encontrada"}, 404

        comunidade["participando"] = comunidadeService.usuarioParticipa(
            usuario_id, comunidade_id
        )

        comunidade["eh_criador"] = (
            int(usuario_id) == int(comunidade["criador_id"])
        )

        comunidade["total_membros"] = comunidadeService.contarMembros(
            comunidade_id
        )

        return comunidade


    # COMUNIDADES DO USUÁRIO

    @app.route("/buscarComunidadeUsuario", methods=["GET"])
    def buscarComunidadeUsuario():

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        usuario_id = session["user.id"]

        return comunidadeService.listarTodasComunidadesDoUsuario(usuario_id)


    # FILTRAR POR GÊNERO

    @app.route("/filtroGeneroComunidade/<string:genero>", methods=["GET"])
    def filtroGeneroComunidade(genero):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        return comunidadeService.filtroComunidadesPorGenero(genero)


    # ENTRAR NA COMUNIDADE

    @app.route("/entrarComunidade/<int:comunidade_id>", methods=["POST"])
    def entrarComunidade(comunidade_id):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        usuario_id = session["user.id"]

        resultado = comunidadeService.entrarComunidade(
            usuario_id,
            comunidade_id
        )

        if resultado == "COMUNIDADE_NAO_ENCONTRADA":
            return {"erro": "Comunidade não encontrada"}, 404

        if resultado == "USUARIO_BLOQUEADO":
            return {
                "erro": "Você foi bloqueado pelo criador desta comunidade"
            }, 403

        if resultado == "JA_PARTICIPA":
            return {
                "erro": "Você já participa desta comunidade"
            }, 409

        if resultado != "SUCESSO":
            return {
                "erro": "Não foi possível entrar na comunidade"
            }, 500

        return {
            "mensagem": "Entrou na comunidade com sucesso"
        }, 200


    # SAIR DA COMUNIDADE

    @app.route("/sairComunidade/<int:comunidade_id>", methods=["POST"])
    def sairComunidade(comunidade_id):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        usuario_id = session["user.id"]

        saiu = comunidadeService.sairComunidade(
            usuario_id,
            comunidade_id
        )

        if not saiu:
            return {
                "erro": "Você não participa desta comunidade"
            }, 400

        return {"mensagem": "Saiu da comunidade com sucesso"}, 200


    # PESQUISAR COMUNIDADES PELO NOME

    @app.route("/buscarComunidades", methods=["GET"])
    def buscarComunidades():

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        nome = request.args.get("nome", "")

        comunidades = comunidadeService.buscarComunidades(nome)

        for comunidade in comunidades:
            comunidade["total_membros"] = comunidadeService.contarMembros(
                comunidade["id"]
            )

        return comunidades


    # BUSCAR COMUNIDADES DE UM USUÁRIO PELO ID

    @app.route("/comunidadesUsuario/<int:usuario_id>", methods=["GET"])
    def comunidadesUsuario(usuario_id):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        comunidades = comunidadeService.listarTodasComunidadesDoUsuario(
            usuario_id
        )

        for comunidade in comunidades:
            comunidade["total_membros"] = comunidadeService.contarMembros(
                comunidade["id"]
            )

        return comunidades, 200


    # BLOQUEAR PARTICIPANTE

    @app.route(
        "/comunidade/<int:comunidade_id>/bloquear/<int:usuario_id>",
        methods=["POST"]
    )
    def bloquearParticipante(comunidade_id, usuario_id):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        criador_id = int(session["user.id"])

        comunidade = comunidadeService.listarComunidade(comunidade_id)

        if comunidade is None:
            return {"erro": "Comunidade não encontrada"}, 404

        if criador_id != int(comunidade["criador_id"]):
            return {
                "erro": "Somente o criador pode bloquear participantes"
            }, 403

        if criador_id == usuario_id:
            return {"erro": "Você não pode bloquear a si mesmo"}, 400

        if comunidadeService.usuarioBloqueado(usuario_id, comunidade_id):
            return {"erro": "Este usuário já está bloqueado"}, 409

        bloqueado = comunidadeService.bloquearUsuario(
            comunidade_id,
            usuario_id,
            criador_id
        )

        if not bloqueado:
            return {
                "erro": "Usuário não participa desta comunidade"
            }, 400

        return {"mensagem": "Usuário bloqueado com sucesso"}, 200


    # DESBLOQUEAR PARTICIPANTE

    @app.route(
        "/comunidade/<int:comunidade_id>/desbloquear/<int:usuario_id>",
        methods=["DELETE"]
    )
    def desbloquearParticipante(comunidade_id, usuario_id):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        criador_id = int(session["user.id"])

        comunidade = comunidadeService.listarComunidade(comunidade_id)

        if comunidade is None:
            return {"erro": "Comunidade não encontrada"}, 404

        if criador_id != int(comunidade["criador_id"]):
            return {
                "erro": "Somente o criador pode desbloquear participantes"
            }, 403

        desbloqueado = comunidadeService.desbloquearUsuario(
            comunidade_id,
            usuario_id
        )

        if not desbloqueado:
            return {"erro": "Usuário não está bloqueado"}, 404

        return {"mensagem": "Usuário desbloqueado com sucesso"}, 200


    # LISTAR USUÁRIOS BLOQUEADOS

    @app.route(
        "/comunidade/<int:comunidade_id>/bloqueados",
        methods=["GET"]
    )
    def listarBloqueados(comunidade_id):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        comunidade = comunidadeService.listarComunidade(comunidade_id)

        if comunidade is None:
            return {"erro": "Comunidade não encontrada"}, 404

        if int(session["user.id"]) != int(comunidade["criador_id"]):
            return {"erro": "Não autorizado"}, 403

        return comunidadeService.listarUsuariosBloqueados(
            comunidade_id
        ), 200


    # LISTAR PARTICIPANTES DA COMUNIDADE

    @app.route(
        "/comunidade/<int:comunidade_id>/participantes",
        methods=["GET"]
    )
    def listarParticipantes(comunidade_id):

        if "user.id" not in session:
            return {"erro": "Não autenticado"}, 401

        comunidade = comunidadeService.listarComunidade(comunidade_id)

        if comunidade is None:
            return {"erro": "Comunidade não encontrada"}, 404

        if int(session["user.id"]) != int(comunidade["criador_id"]):
            return {
                "erro": "Somente o criador pode visualizar os participantes"
            }, 403

        participantes = comunidadeService.listarParticipantes(
            comunidade_id
        )

        return participantes, 200