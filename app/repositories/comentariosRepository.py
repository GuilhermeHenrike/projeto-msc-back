from database import conectar


class ComentarioRepository:

    def salvarComentario(self, comentario):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO comentarios
                    (usuario_id, publicacao_id, texto)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (
                    comentario.usuario_id,
                    comentario.publicacao_id,
                    comentario.texto
                ))

                comentario.id = cursor.fetchone()["id"]

            conexao.commit()
            return comentario

        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()
            

    def carregarComentarios(self, publicacao_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        comentarios.id,
                        comentarios.usuario_id,
                        comentarios.publicacao_id,
                        comentarios.texto,
                        comentarios.data_criacao,
                        comentarios.data_atualizacao,
                        usuarios.nome AS nome_usuario,
                        usuarios.foto_url
                    FROM comentarios
                    INNER JOIN usuarios
                        ON comentarios.usuario_id = usuarios.id
                    WHERE comentarios.publicacao_id = %s
                    ORDER BY comentarios.data_criacao ASC
                """, (publicacao_id,))

                return cursor.fetchall()
        finally:
            conexao.close()


    def editarComentario(self, comentario_id, usuario_id, texto):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    UPDATE comentarios
                    SET texto = %s,
                        data_atualizacao = CURRENT_TIMESTAMP
                    WHERE id = %s
                    AND usuario_id = %s
                """, (texto, comentario_id, usuario_id))

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()


    def apagarComentario(self, comentario_id, usuario_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM comentarios
                    WHERE id = %s
                    AND usuario_id = %s
                """, (comentario_id, usuario_id))

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()