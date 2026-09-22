from database import conectar

class PerfilRepository:

    def buscarPerfil(self, usuario_id):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT id, nome, foto_url
            FROM usuarios
            WHERE id = %s
        """

        cursor.execute(sql, (usuario_id,))

        usuario = cursor.fetchone()

        cursor.close()
        conexao.close()

        return usuario
    

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