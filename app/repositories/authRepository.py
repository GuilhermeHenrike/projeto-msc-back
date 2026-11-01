from database import conectar

class AuthRepository:

    def salvarUser(self, user):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO usuarios(nome, email, senha_hash)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (user.nome, user.email, user.senha_hash))

                user.id = cursor.fetchone()["id"]

            conexao.commit()
            return user

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


    def procurarEmail(self, email):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT id, nome, email, senha_hash, foto_url
                    FROM usuarios
                    WHERE email = %s
                """, (email,))

                return cursor.fetchone()

        finally:
            conexao.close()


    def procurarNome(self, nome):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT id, nome, email, senha_hash
                    FROM usuarios
                    WHERE nome = %s
                """, (nome,))

                return cursor.fetchone()

        finally:
            conexao.close()