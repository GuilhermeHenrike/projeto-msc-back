from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:

    def __init__(self, repoAuth):
        self.repoAuth = repoAuth

    def fazerRegistro(self, nome, email, senha):

        if len(senha) < 8:
            return "SENHA_CURTA"

        senhaHash = generate_password_hash(senha)

        novoUser = Usuario(nome, email, senhaHash, None)
        self.repoAuth.salvarUser(novoUser)


    def fazerLogin(self, email, senha):

        resultado = self.repoAuth.procurarEmail(email)

        if resultado and check_password_hash(resultado["senha_hash"], senha):
            return Usuario(
                resultado["nome"],
                resultado["email"],
                resultado["senha_hash"],
                resultado["id"],
                resultado["foto_url"]
            )

        return None