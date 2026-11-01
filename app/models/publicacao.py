
class Publicacao:
    def __init__( self, usuario_id, comunidade_id, legenda=None, imagem_url=None, tipo_midia="imagem", status_moderacao="aprovada", id=None):
        self.id = id
        self.usuario_id = usuario_id
        self.comunidade_id = comunidade_id
        self.legenda = legenda
        self.imagem_url = imagem_url
        self.tipo_midia = tipo_midia
        self.status_moderacao = status_moderacao
