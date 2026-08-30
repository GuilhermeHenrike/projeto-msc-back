from flask import redirect,request, session

def publicacaoController(app, publicacaoService):

    @app.route("/publicacao", methods = ["POST"])
    def criarPublicacao():

        if "user.id" not in session:
            return redirect("/")

        imagem = request.files.get("imagem")
        legenda = request.form.get("legenda")
        comunidade_id = request.form.get("comunidade")

        if not imagem:
            return "selecione uma imagem"

        usuario_id = session["user.id"]

        publicacaoService.criarPublicacao(imagem, legenda, usuario_id, comunidade_id)

        return redirect("/home")