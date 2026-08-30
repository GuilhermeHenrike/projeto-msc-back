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