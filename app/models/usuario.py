class Usuario:

    def __init__(self, nome, email, senha_hash, id=None, foto_url=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.foto_url = foto_url
