from database import conectar


class AlbumRepository:

    def buscarAlbumPorDeezerId(self, deezer_id):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT *
            FROM albuns
            WHERE deezer_id = %s
        """

        cursor.execute(sql, (deezer_id,))

        album = cursor.fetchone()

        cursor.close()
        conexao.close()

        return album


    def salvarAlbum(self, album):

        album_existente = self.buscarAlbumPorDeezerId(album.deezer_id)

        if album_existente:
            return album_existente

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            INSERT INTO albuns
            (deezer_id, titulo, artista, capa_url)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (
            album.deezer_id,
            album.titulo,
            album.artista,
            album.capa_url
        ))

        album.id = cursor.lastrowid

        conexao.commit()

        cursor.close()
        conexao.close()

        return album


    def carregarAlbum(self, album_id):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT *
            FROM albuns
            WHERE id = %s
        """

        cursor.execute(sql, (album_id,))

        album = cursor.fetchone()

        cursor.close()
        conexao.close()

        return album