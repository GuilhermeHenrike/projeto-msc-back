from database import conectar

class CurtidaRepository:

    # Adicionar curtida
    def curtir(self, usuario_id, publicacao_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO curtidas (usuario_id, publicacao_id)
                    VALUES (%s, %s)
                """, (usuario_id, publicacao_id))

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


    # Remover curtida
    def descurtir(self, usuario_id, publicacao_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM curtidas
                    WHERE usuario_id = %s
                    AND publicacao_id = %s
                """, (usuario_id, publicacao_id))

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


    # Verificar se o usuário já curtiu
    def verificarCurtida(self, usuario_id, publicacao_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT id
                    FROM curtidas
                    WHERE usuario_id = %s
                    AND publicacao_id = %s
                    LIMIT 1
                """, (usuario_id, publicacao_id))

                return cursor.fetchone()

        finally:
            conexao.close()


    # Contar curtidas da publicação
    def contarCurtidas(self, publicacao_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) AS total
                    FROM curtidas
                    WHERE publicacao_id = %s
                """, (publicacao_id,))

                resultado = cursor.fetchone()

                return resultado["total"]

        finally:
            conexao.close()