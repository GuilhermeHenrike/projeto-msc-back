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