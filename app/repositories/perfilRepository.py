from database import conectar

class PerfilRepository:

    def editarPerfil(self, user):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            UPDATE usuarios
            SET nome = %s, foto_url = %s
            WHERE id = %s
        """

        cursor.execute(sql, (user.nome, user.foto_url, user.id))

        conexao.commit()

        cursor.close()
        conexao.close()

        return user

    def buscarUsuario(self, usuario_id):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT
                id,
                nome,
                foto_url
            FROM usuarios
            WHERE id = %s
        """

        cursor.execute(sql, (usuario_id,))

        usuario = cursor.fetchone()

        cursor.close()
        conexao.close()

        return usuario


    def buscarPublicacoesUsuario(self, usuario_id):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
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
        """

        cursor.execute(sql, (usuario_id,))

        publicacoes = cursor.fetchall()

        cursor.close()
        conexao.close()

        return publicacoes