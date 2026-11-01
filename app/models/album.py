class Album:
    def __init__(self, deezer_id, titulo, artista, capa_url, id=None):
        self.id = id
        self.deezer_id = deezer_id
        self.titulo = titulo
        self.artista = artista
        self.capa_url = capa_url