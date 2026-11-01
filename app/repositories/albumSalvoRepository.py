from database import conectar

class AlbumSalvoRepository:

    def salvarAlbumUsuario(self, usuario_id, album_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    INSERT INTO albuns_salvos
                    (usuario_id, album_id)
                    VALUES (%s, %s)
                """

                cursor.execute(sql, (usuario_id, album_id))

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


    def removerAlbumUsuario(self, usuario_id, album_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    DELETE FROM albuns_salvos
                    WHERE usuario_id = %s
                    AND album_id = %s
                """

                cursor.execute(sql, (usuario_id, album_id))

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


    def carregarAlbunsSalvos(self, usuario_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
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
                return cursor.fetchall()

        finally:
            conexao.close()