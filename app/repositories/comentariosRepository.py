from database import conectar


class ComentarioRepository:

    def salvarComentario(self, comentario):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            INSERT INTO comentarios
            (usuario_id, publicacao_id, texto)
            VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (
            comentario.usuario_id,
            comentario.publicacao_id,
            comentario.texto
        ))

        comentario.id = cursor.lastrowid

        conexao.commit()

        cursor.close()
        conexao.close()

        return comentario


    def carregarComentarios(self, publicacao_id):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
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
        """

        cursor.execute(sql, (publicacao_id,))

        comentarios = cursor.fetchall()

        cursor.close()
        conexao.close()

        return comentarios


    def editarComentario(self, comentario_id, usuario_id, texto):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            UPDATE comentarios
            SET texto = %s
            WHERE id = %s
            AND usuario_id = %s
        """

        cursor.execute(sql, (
            texto,
            comentario_id,
            usuario_id
        ))

        conexao.commit()

        cursor.close()
        conexao.close()


    def apagarComentario(self, comentario_id, usuario_id):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            DELETE FROM comentarios
            WHERE id = %s
            AND usuario_id = %s
        """

        cursor.execute(sql, (
            comentario_id,
            usuario_id
        ))

        conexao.commit()

        cursor.close()
        conexao.close()