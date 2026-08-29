class Comunidade:

    def __init__(self, nome, criador_id=None, descricao=None, imagem_url=None, id=None):
        self.id = id
        self.nome = nome
        self.criador_id = criador_id
        self.descricao = descricao
        self.imagem_url = imagem_url
