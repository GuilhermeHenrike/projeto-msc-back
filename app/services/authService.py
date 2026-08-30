from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
import random
from flask import redirect, request, session

class AuthService:

    def __init__(self, repoUser, mail):
        self.repoUser = repoUser
        self.mail = mail

    def fazerRegistro(self, nome, email, senha):

        senhaHash = generate_password_hash(senha)

        novoUser = Usuario(nome, email, senhaHash, None)
        self.repoUser.salvarUser(novoUser)


    def fazerLogin(self, email, senha):

        resultado = self.repoUser.procurarEmail(email)


        if resultado and check_password_hash(resultado["senha_hash"], senha):
            return Usuario(
                resultado["nome"],
                resultado["email"],
                resultado["senha_hash"],
                resultado["id"],
                resultado["foto_url"]
            )

        return None

    def enviarCodigo(self,email):

        UsuarioEmail = self.repoUser.procurarEmail(email)

        if not Usuario:
            return False

        codigoAleatorio = random.randint(100000, 999999)

        session["codigo_recuperacao"] = str(codigoAleatorio)
        session["email_recuperacao"] = email

        mensagem = Message(
            subject='codigo de verificação',
            recipients=[email]
        )

        mensagem.body=f"esse é seu cod: {codigoAleatorio}"

        self.mail.send(mensagem)


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

        nsenha = self.repoUser.atualizarSenha(email, senhaHash)
        
        if nsenha:
            session.pop("codigo_verificado", None)
            session.pop("codigo_recuperacao", None)
            session.pop("email_recuperacao", None)
            return True

        return False


           
            