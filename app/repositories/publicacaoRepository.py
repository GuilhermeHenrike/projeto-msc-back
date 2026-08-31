from database import conectar


class PublicacaoRepository:

    def salvarPublicacao(self, publicacao):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            INSERT INTO publicacoes
            (usuario_id, comunidade_id, legenda, imagem_url, status_moderacao)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            publicacao.usuario_id,
            publicacao.comunidade_id,
            publicacao.legenda,
            publicacao.imagem_url,
            publicacao.status_moderacao
        ))

        publicacao.id = cursor.lastrowid

        conexao.commit()

        cursor.close()
        conexao.close()

        return publicacao


    def carregarPublicacoes(self):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT publicacoes.*, usuarios.nome AS nome_usuario
            FROM publicacoes
            JOIN usuarios ON publicacoes.usuario_id = usuarios.id
            ORDER BY publicacoes.data_criacao DESC
        """

        cursor.execute(sql)

        publicacoes = cursor.fetchall()

        cursor.close()
        conexao.close()

        return publicacoes


    def buscarPublicacao(self, publicacao_id):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT *
            FROM publicacoes
            WHERE id = %s
        """

        cursor.execute(sql, (publicacao_id,))

        publicacao = cursor.fetchone()

        cursor.close()
        conexao.close()

        return publicacao


    def apagarPublicacao(self, publicacao_id):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            DELETE FROM publicacoes
            WHERE id = %s
        """

        cursor.execute(sql, (publicacao_id,))

        conexao.commit()

        cursor.close()
        conexao.close()