from database import conectar


class AvaliacaoRepository:

    def salvarAvaliacao(self, avaliacao):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            INSERT INTO avaliacoes
            (usuario_id, album_id, nota)
            VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (
            avaliacao.usuario_id,
            avaliacao.album_id,
            avaliacao.nota
        ))

        avaliacao.id = cursor.lastrowid

        conexao.commit()

        cursor.close()
        conexao.close()

        return avaliacao


    def buscarAvaliacao(self, usuario_id, album_id):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT *
            FROM avaliacoes
            WHERE usuario_id = %s
            AND album_id = %s
        """

        cursor.execute(sql, (usuario_id, album_id))

        avaliacao = cursor.fetchone()

        cursor.close()
        conexao.close()

        return avaliacao


    def atualizarAvaliacao(self, usuario_id, album_id, nota):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            UPDATE avaliacoes
            SET nota = %s
            WHERE usuario_id = %s
            AND album_id = %s
        """

        cursor.execute(sql, (nota, usuario_id, album_id))

        conexao.commit()

        linhas_afetadas = cursor.rowcount

        cursor.close()
        conexao.close()

        return linhas_afetadas > 0


    def carregarAvaliacoesUsuario(self, usuario_id):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
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
        """

        cursor.execute(sql, (usuario_id,))

        avaliacoes = cursor.fetchall()

        cursor.close()
        conexao.close()

        return avaliacoes