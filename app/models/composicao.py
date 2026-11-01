
class Composicao:
    def __init__(
        self,
        usuario_id,
        titulo,
        estilo_musical,
        letra,
        id=None,
        publica=False
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.estilo_musical = estilo_musical
        self.letra = letra
        self.publica = publica
