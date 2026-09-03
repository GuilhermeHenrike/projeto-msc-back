from database import conectar


class CurtidaRepository:

    def curtir(self, usuario_id, publicacao_id):
        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            INSERT INTO curtidas (usuario_id, publicacao_id)
            VALUES (%s, %s)
        """

        cursor.execute(sql, (usuario_id, publicacao_id))

        conexao.commit()
        cursor.close()
        conexao.close()


    def descurtir(self, usuario_id, publicacao_id):
        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            DELETE FROM curtidas
            WHERE usuario_id = %s
            AND publicacao_id = %s
        """

        cursor.execute(sql, (usuario_id, publicacao_id))

        conexao.commit()
        cursor.close()
        conexao.close()


    def verificarCurtida(self, usuario_id, publicacao_id):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT id
            FROM curtidas
            WHERE usuario_id = %s
            AND publicacao_id = %s
        """

        cursor.execute(sql, (usuario_id, publicacao_id))

        curtida = cursor.fetchone()

        cursor.close()
        conexao.close()

        return curtida


    def contarCurtidas(self, publicacao_id):
        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            SELECT COUNT(*) AS total
            FROM curtidas
            WHERE publicacao_id = %s
        """

        cursor.execute(sql, (publicacao_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conexao.close()

        return resultado[0]