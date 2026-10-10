from database import conectar


class PerfilRepository:

    def editarPerfil(self, user):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    UPDATE usuarios
                    SET nome = %s,
                        foto_url = %s
                    WHERE id = %s
                """, (user.nome, user.foto_url, user.id))

            conexao.commit()
            return user

        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()
            

    def buscarUsuario(self, usuario_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT id, nome, foto_url
                    FROM usuarios
                    WHERE id = %s
                """, (usuario_id,))

                return cursor.fetchone()
        finally:
            conexao.close()


    def buscarPublicacoesUsuario(self, usuario_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        publicacoes.*,
                        usuarios.nome AS nome_usuario,
                        usuarios.foto_url,
                        (
                            SELECT COUNT(*)
                            FROM curtidas
                            WHERE curtidas.publicacao_id = publicacoes.id
                        ) AS total_curtidas,
                        (
                            SELECT COUNT(*)
                            FROM comentarios
                            WHERE comentarios.publicacao_id = publicacoes.id
                        ) AS total_comentarios
                    FROM publicacoes
                    JOIN usuarios
                        ON publicacoes.usuario_id = usuarios.id
                    WHERE publicacoes.usuario_id = %s
                    ORDER BY publicacoes.id DESC
                """, (usuario_id,))

                return cursor.fetchall()
        finally:
            conexao.close()