from database import conectar

class SenhaRepository:

    def atualizarSenha(self, email, senhaHash):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    UPDATE usuarios
                    SET senha_hash = %s
                    WHERE email = %s
                """, (senhaHash, email))

                linhasAlteradas = cursor.rowcount

            conexao.commit()
            return linhasAlteradas > 0

        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()


    def atualizarSenhaPerfil(self, usuario_id, senhaHash):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    UPDATE usuarios
                    SET senha_hash = %s
                    WHERE id = %s
                """, (senhaHash, usuario_id))

                linhasAlteradas = cursor.rowcount

            conexao.commit()
            return linhasAlteradas > 0

        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()


    def procurarId(self, usuario_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT senha_hash
                    FROM usuarios
                    WHERE id = %s
                """, (usuario_id,))

                return cursor.fetchone()

        finally:
            conexao.close()