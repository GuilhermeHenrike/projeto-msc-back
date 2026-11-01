from database import conectar

class AvaliacaoRepository:

    def salvarAvaliacao(self, avaliacao):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO avaliacoes
                    (usuario_id, album_id, nota)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (
                    avaliacao.usuario_id,
                    avaliacao.album_id,
                    avaliacao.nota
                ))

                avaliacao.id = cursor.fetchone()["id"]

            conexao.commit()
            return avaliacao

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


    def buscarAvaliacao(self, usuario_id, album_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT *
                    FROM avaliacoes
                    WHERE usuario_id = %s
                    AND album_id = %s
                """, (usuario_id, album_id))

                return cursor.fetchone()

        finally:
            conexao.close()


    def atualizarAvaliacao(self, usuario_id, album_id, nota):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    UPDATE avaliacoes
                    SET nota = %s
                    WHERE usuario_id = %s
                    AND album_id = %s
                """, (nota, usuario_id, album_id))

                linhas_afetadas = cursor.rowcount

            conexao.commit()
            return linhas_afetadas > 0

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


    def carregarAvaliacoesUsuario(self, usuario_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        avaliacoes.id AS avaliacao_id,
                        avaliacoes.nota,
                        avaliacoes.data_criacao,
                        avaliacoes.data_atualizacao,
                        albuns.id AS album_id,
                        albuns.deezer_id,
                        albuns.titulo,
                        albuns.artista,
                        albuns.capa_url

                    FROM avaliacoes

                    JOIN albuns
                        ON avaliacoes.album_id = albuns.id

                    WHERE avaliacoes.usuario_id = %s

                    ORDER BY avaliacoes.data_atualizacao DESC
                """, (usuario_id,))

                return cursor.fetchall()

        finally:
            conexao.close()