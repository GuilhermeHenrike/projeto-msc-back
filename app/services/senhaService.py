import os
import random
import requests

from flask import session
from werkzeug.security import generate_password_hash, check_password_hash


class SenhaService:

    def __init__(self, repoSenha, repoAuth):
        self.repoSenha = repoSenha
        self.repoAuth = repoAuth

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

        api_key = os.getenv("BREVO_API_KEY")
        remetente = os.getenv("BREVO_FROM_EMAIL")

        if not api_key or not remetente:
            print("Erro: variáveis da Brevo não configuradas.")
            return False

        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        }

        dados = {
            "sender": {
                "name": "Yrplace",
                "email": remetente
            },
            "to": [
                {
                    "email": email
                }
            ],
            "subject": "Código de recuperação de senha - Yrplace",
            "htmlContent": f"""
                <div style="font-family: Arial, sans-serif; color: #333;">
                    <h2>Recuperação de senha</h2>

                    <p>
                        Você solicitou a recuperação da sua senha no Yrplace.
                    </p>

                    <p>Seu código de verificação é:</p>

                    <h1 style="color: #7c3aed; font-size: 32px;">
                        {codigoAleatorio}
                    </h1>

                    <p>
                        Não compartilhe este código com ninguém.
                    </p>

                    <p>
                        Se você não solicitou a recuperação,
                        ignore este e-mail.
                    </p>
                </div>
            """
        }

        try:
            resposta = requests.post(
                url,
                headers=headers,
                json=dados,
                timeout=15
            )

            resposta.raise_for_status()

            session["codigo_recuperacao"] = str(codigoAleatorio)
            session["email_recuperacao"] = email

            session.pop("codigo_verificado", None)

            print("E-mail de recuperação enviado pela Brevo.")

            return True

        except requests.exceptions.RequestException as erro:
            print(f"Erro ao enviar e-mail pela Brevo: {erro}")

            return False

    def confirmarCodigo(self, codigo_digitado):
        codigoSalvo = session.get("codigo_recuperacao")

        if not codigoSalvo:
            return False

        if str(codigo_digitado).strip() == str(codigoSalvo).strip():
            session["codigo_verificado"] = True

            return True

        return False

    def mudarSenha(self, nova_senha, email):
        if not nova_senha or not email:
            return False

        if len(nova_senha) < 8:
            return "SENHA_CURTA"

        if not session.get("codigo_verificado"):
            return False

        emailRecuperacao = session.get("email_recuperacao")

        if email != emailRecuperacao:
            return False

        senhaHash = generate_password_hash(nova_senha)

        sucesso = self.repoSenha.atualizarSenha(
            email,
            senhaHash
        )

        if sucesso:
            session.pop("codigo_verificado", None)
            session.pop("codigo_recuperacao", None)
            session.pop("email_recuperacao", None)

            return True

        return False


    def mudarSenhaPerfil(self, nova_senha, usuario_id):
        if not nova_senha or not usuario_id:
            return False

        if len(nova_senha) < 8:
            return "SENHA_CURTA"

        senhaHash = generate_password_hash(nova_senha)

        return self.repoSenha.atualizarSenhaPerfil(
            usuario_id,
            senhaHash
        )