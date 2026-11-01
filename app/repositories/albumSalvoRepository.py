from database import conectar


class AlbumSalvoRepository:

    def salvarAlbumUsuario(self, usuario_id, album_id):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            INSERT INTO albuns_salvos
            (usuario_id, album_id)
            VALUES (%s, %s)
        """

        cursor.execute(sql, (usuario_id, album_id))

        conexao.commit()

        cursor.close()
        conexao.close()


    def removerAlbumUsuario(self, usuario_id, album_id):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            DELETE FROM albuns_salvos
            WHERE usuario_id = %s
            AND album_id = %s
        """

        cursor.execute(sql, (usuario_id, album_id))

        conexao.commit()

        cursor.close()
        conexao.close()


    def carregarAlbunsSalvos(self, usuario_id):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT
                albuns.*,
                albuns_salvos.data_criacao AS data_salvamento
            FROM albuns_salvos

            JOIN albuns
                ON albuns_salvos.album_id = albuns.id

            WHERE albuns_salvos.usuario_id = %s

            ORDER BY albuns_salvos.data_criacao DESC
        """

        cursor.execute(sql, (usuario_id,))

        albuns = cursor.fetchall()

        cursor.close()
        conexao.close()

        return albuns