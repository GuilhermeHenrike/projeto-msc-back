from database import conectar

class AuthRepository:

    def salvarUser(self, user):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            INSERT INTO usuarios(nome, email, senha_hash)
            VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (user.nome, user.email, user.senha_hash))
        conexao.commit()

        user.id = cursor.lastrowid

        conexao.close()
        cursor.close()

        return user

    def procurarEmail(self, email):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT id, nome, email, senha_hash, foto_url
            FROM usuarios
            WHERE email = %s
        """

        cursor.execute(sql, (email,))
        resultado = cursor.fetchone()

        conexao.close()
        cursor.close()

        return resultado

    def procurarNome(self, nome):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT id, nome, email, senha_hash
            FROM usuarios
            WHERE nome = %s
        """

        cursor.execute(sql, (nome,))
        resultado = cursor.fetchone()

        conexao.close()
        cursor.close()

        return resultado


    def atualizarSenha(self, email, senhaHash):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            UPDATE usuarios
            SET senha_hash = %s
            WHERE email = %s
            """

        cursor.execute(sql, (senhaHash, email))

        conexao.commit()

        linhasAlteradas = cursor.rowcount

        cursor.close()
        conexao.close()

        return linhasAlteradas > 0
