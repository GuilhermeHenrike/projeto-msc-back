
from database import conectar


class CurtidaRepository:

    # Adicionar curtida
    def curtir(self, usuario_id, publicacao_id):
        conexao = conectar()
        cursor = conexao.cursor()

        try:
            sql = """
                INSERT INTO curtidas (usuario_id, publicacao_id)
                VALUES (%s, %s)
            """

            cursor.execute(sql, (usuario_id, publicacao_id))
            conexao.commit()

        finally:
            cursor.close()
            conexao.close()

    # Remover curtida
    def descurtir(self, usuario_id, publicacao_id):
        conexao = conectar()
        cursor = conexao.cursor()

        try:
            sql = """
                DELETE FROM curtidas
                WHERE usuario_id = %s
                AND publicacao_id = %s
            """

            cursor.execute(sql, (usuario_id, publicacao_id))
            conexao.commit()

        finally:
            cursor.close()
            conexao.close()

    # Verificar se o usuário já curtiu
    def verificarCurtida(self, usuario_id, publicacao_id):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT id
                FROM curtidas
                WHERE usuario_id = %s
                AND publicacao_id = %s
                LIMIT 1
            """

            cursor.execute(sql, (usuario_id, publicacao_id))

            return cursor.fetchone()

        finally:
            cursor.close()
            conexao.close()

    # Contar curtidas da publicação
    def contarCurtidas(self, publicacao_id):
        conexao = conectar()
        cursor = conexao.cursor()

        try:
            sql = """
                SELECT COUNT(*) AS total
                FROM curtidas
                WHERE publicacao_id = %s
            """

            cursor.execute(sql, (publicacao_id,))

            resultado = cursor.fetchone()

            return resultado[0]

        finally:
            cursor.close()
            conexao.close()
