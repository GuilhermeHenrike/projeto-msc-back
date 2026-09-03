from database import conectar

class ComunidadeRepository:

    def salvarComunidade(self, comunidade):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            INSERT INTO comunidades
            (nome, genero, descricao, imagem_url, criador_id)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (comunidade.nome, comunidade.genero, comunidade.descricao,
            comunidade.imagem_url, comunidade.criador_id
        ))

        comunidade.id = cursor.lastrowid

        sql = """
            INSERT INTO membros_comunidade
            (usuario_id, comunidade_id)
            VALUES (%s, %s)
        """

        cursor.execute(sql, (
            comunidade.criador_id,
            comunidade.id
        ))

        conexao.commit()

        cursor.close()
        conexao.close()

        return comunidade


    
    def editarComunidade(self, comunidade, comunidade_id):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            UPDATE comunidades
            SET nome = %s,
                genero = %s,
                descricao = %s,
                imagem_url = %s
            WHERE id = %s
        """

        cursor.execute(sql, (comunidade.nome, comunidade.genero, comunidade.descricao,
            comunidade.imagem_url, comunidade_id
        ))

        conexao.commit()

        cursor.close()
        conexao.close()

        return comunidade



    def apagarComunidade(self, comunidade_id):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            DELETE FROM comunidades
            WHERE id = %s
        """

        cursor.execute(sql, (comunidade_id,))
        conexao.commit()

        cursor.close()
        conexao.close()



    ## BUSCAR COMUNIDADES


    def todasComunidades(self, usuario_id):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT c.*
            FROM comunidades c
            LEFT JOIN membros_comunidade mc
                ON c.id = mc.comunidade_id
                AND mc.usuario_id = %s
            WHERE mc.id IS NULL
        """

        cursor.execute(sql, (usuario_id,))
        comunidades = cursor.fetchall()

        cursor.close()
        conexao.close()

        return comunidades



    def buscarComunidade(self, comunidade_id):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT * FROM comunidades
            WHERE id = %s
        """

        cursor.execute(sql, (comunidade_id,))
        comunidade = cursor.fetchone()

        cursor.close()
        conexao.close()

        return comunidade



    def todasComunidadesPorUsuario(self, usuario_id):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT c.*
            FROM comunidades c
            INNER JOIN membros_comunidade mc
                ON c.id = mc.comunidade_id
            WHERE mc.usuario_id = %s
        """

        cursor.execute(sql, (usuario_id,))
        comunidades = cursor.fetchall()

        cursor.close()
        conexao.close()

        return comunidades


    ## FILTRO COMUNIDADE POR GENERO

    def comunidadesPorGenero(self, genero):

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT *
            FROM comunidades
            WHERE genero = %s
        """

        cursor.execute(sql, (genero,))
        comunidades = cursor.fetchall()

        cursor.close()
        conexao.close()

        return comunidades


    ## ENTRAR E SAIR DA COMUNIDADE


    def entrarComunidade(self, usuario_id, comunidade_id):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            INSERT INTO membros_comunidade
            (usuario_id, comunidade_id)
            VALUES (%s, %s)
        """

        cursor.execute(sql, (usuario_id, comunidade_id))
        conexao.commit()

        cursor.close()
        conexao.close()


    def sairComunidade(self, usuario_id, comunidade_id):

        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            DELETE FROM membros_comunidade
            WHERE usuario_id = %s
            AND comunidade_id = %s
        """

        cursor.execute(sql, (usuario_id, comunidade_id))
        conexao.commit()

        cursor.close()
        conexao.close()