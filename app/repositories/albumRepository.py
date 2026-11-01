from database import conectar

class AlbumRepository:

    def buscarAlbumPorDeezerId(self, deezer_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    SELECT *
                    FROM albuns
                    WHERE deezer_id = %s
                """

                cursor.execute(sql, (deezer_id,))
                return cursor.fetchone()

        finally:
            conexao.close()


    def salvarAlbum(self, album):
        album_existente = self.buscarAlbumPorDeezerId(album.deezer_id)

        if album_existente:
            return album_existente

        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    INSERT INTO albuns
                    (deezer_id, titulo, artista, capa_url)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """

                cursor.execute(sql, (
                    album.deezer_id,
                    album.titulo,
                    album.artista,
                    album.capa_url
                ))

                album.id = cursor.fetchone()["id"]

            conexao.commit()
            return album

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


    def carregarAlbum(self, album_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    SELECT *
                    FROM albuns
                    WHERE id = %s
                """

                cursor.execute(sql, (album_id,))
                return cursor.fetchone()

        finally:
            conexao.close()