from flask import redirect, request, session

def comunidadeController(app, comunidadeService):

    @app.route("/comunidade", methods=["POST"])
    def criarComunidade():

        if "user.id" not in session:
            return redirect("/")

        nome = request.form.get("nome")
        genero = request.form.get("genero")
        descricao = request.form.get("descricao")
        imagem_url = request.form.get("imagem_url")

        usuario_id = session["user.id"]

        comunidadeService.criarComunidade(nome, genero, usuario_id, descricao, imagem_url)

        return redirect("/home")


    @app.route("/comunidade/<int:id>", methods=["PUT"])
    def atualizarComunidade(id):

        if "user.id" not in session:
            return redirect("/")

        comunidade = comunidadeService.listarComunidade(id)

        if comunidade is None:
            return "Comunidade não encontrada", 404

        if session["user.id"] != comunidade["criador_id"]:
            return redirect("/home")

        nome = request.form.get("nome")
        genero = request.form.get("genero")
        descricao = request.form.get("descricao")
        imagem_url = request.form.get("imagem_url")

        comunidadeService.atualizarComunidade(nome, genero, descricao, imagem_url, id)

        return redirect("/home")


    @app.route("/comunidade/<int:id>", methods=["DELETE"])
    def apagarComunidade(id):

        if "user.id" not in session:
            return redirect("/")

        comunidade = comunidadeService.listarComunidade(id)

        if comunidade is None:
            return "Comunidade não encontrada", 404

        if session["user.id"] != comunidade["criador_id"]:
            return redirect("/home")

        comunidadeService.apagarComunidade(id)

        return "", 204


    ## ROTAS DE BUSCA

    @app.route("/buscarTodasComunidades", methods=["GET"])
    def buscarTodasComunidades():

        if "user.id" not in session:
            return redirect("/")

        return comunidadeService.listarTodasComunidades()


    @app.route("/buscarComunidade/<int:comunidade_id>", methods=["GET"])
    def buscarComunidade(comunidade_id):

        if "user.id" not in session:
            return redirect("/")

        comunidade = comunidadeService.listarComunidade(comunidade_id)

        if comunidade is None:
            return "Comunidade não encontrada", 404

        return comunidade


    @app.route("/buscarComunidadeUsuario/<int:usuario_id>", methods=["GET"])
    def buscarComunidadeUsuario(usuario_id):

        if "user.id" not in session:
            return redirect("/")

        return comunidadeService.listarTodasComunidadesDoUsuario(usuario_id)

    
    ## FILTRO

    @app.route("/filtroGeneroComunidade/<string:genero>", methods=["GET"])
    def filtroGeneroComunidade(genero):

        if "user.id" not in session:
            return redirect("/")

        return comunidadeService.filtroComunidadesPorGenero(genero)