from flask import redirect, request, session

def comunidadeController(app, comunidadeService):

    @app.route("/comunidade", methods=["POST"])
    def criarComunidade():

        if "user.id" not in session:
            return redirect("/")

        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        imagem_url = request.form.get("imagem_url")

        usuario_id = session["user.id"]

        comunidadeService.criarComunidade(nome, usuario_id, descricao, imagem_url)

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
        descricao = request.form.get("descricao")
        imagem_url = request.form.get("imagem_url")

        comunidadeService.atualizarComunidade(nome, descricao, imagem_url, id)

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