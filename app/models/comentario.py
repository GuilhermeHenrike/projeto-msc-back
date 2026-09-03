class Comentario:

    def __init__(
        self,
        usuario_id,
        publicacao_id,
        texto,
        id=None,
        data_criacao=None,
        data_atualizacao=None
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.publicacao_id = publicacao_id
        self.texto = texto
        self.data_criacao = data_criacao
        self.data_atualizacao = data_atualizacao