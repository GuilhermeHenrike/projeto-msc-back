class Avaliacao:
    def __init__(self, usuario_id, album_id, nota, id=None):
        self.id = id
        self.usuario_id = usuario_id
        self.album_id = album_id
        self.nota = nota
