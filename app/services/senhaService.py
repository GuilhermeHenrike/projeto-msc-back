from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from flask import session
import random

class SenhaService:

    def __init__(self, repoSenha, repoAuth, mail):
        self.repoSenha = repoSenha
        self.repoAuth = repoAuth
        self.mail = mail


    def confirmarSenhaAtual(self, usuario_id, senha):

        resultado = self.repoSenha.procurarId(usuario_id)

        if resultado and check_password_hash(resultado["senha_hash"], senha):
            return True

        return False


    def enviarCodigo(self, email):
        usuarioEmail = self.repoAuth.procurarEmail(email)

        if not usuarioEmail:
            return False

        codigoAleatorio = random.randint(100000, 999999)

        session["codigo_recuperacao"] = str(codigoAleatorio)
        session["email_recuperacao"] = email

        mensagem = Message(
            subject="codigo de verificação",
            recipients=[email]
        )

        mensagem.body = f"esse é seu cod: {codigoAleatorio}"

        self.mail.send(mensagem)
        return True


    def confirmarCodigo(self, codigo_digitado):

        cod_salvo = session.get("codigo_recuperacao")

        if str(codigo_digitado).strip() == str(cod_salvo).strip():
            session["codigo_verificado"] = True
            return True

        return False


    def mudarSenha(self, nova_senha, email):

        if not session.get("codigo_verificado"):
            return False

        if not nova_senha or not email:
            return False

        senhaHash = generate_password_hash(nova_senha)

        sucesso = self.repoSenha.atualizarSenha(email, senhaHash)

        if sucesso:
            session.pop("codigo_verificado", None)
            session.pop("codigo_recuperacao", None)
            session.pop("email_recuperacao", None)
            return True

        return False


    def mudarSenhaPerfil(self, nova_senha, usuario_id):

        if not nova_senha or not usuario_id:
            return False

        senhaHash = generate_password_hash(nova_senha)

        return self.repoSenha.atualizarSenhaPerfil(usuario_id, senhaHash)