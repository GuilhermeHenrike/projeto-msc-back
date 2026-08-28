from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash, check_password_hash

print("AUTH SERVICE CARREGADO:", __file__)

class AuthService:

    def __init__(self, repoUser):
        self.repoUser = repoUser

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