from database import conectar

class ComunidadeRepository:

    def salvarComunidade(self, comunidade):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO comunidades
                    (nome, genero, descricao, imagem_url, criador_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    comunidade.nome,
                    comunidade.genero,
                    comunidade.descricao,
                    comunidade.imagem_url,
                    comunidade.criador_id
                ))

                comunidade.id = cursor.fetchone()["id"]

                cursor.execute("""
                    INSERT INTO membros_comunidade
                    (usuario_id, comunidade_id)
                    VALUES (%s, %s)
                """, (
                    comunidade.criador_id,
                    comunidade.id
                ))

            conexao.commit()
            return comunidade

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


    def editarComunidade(self, comunidade, comunidade_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    UPDATE comunidades
                    SET nome = %s,
                        genero = %s,
                        descricao = %s,
                        imagem_url = %s
                    WHERE id = %s
                """, (
                    comunidade.nome,
                    comunidade.genero,
                    comunidade.descricao,
                    comunidade.imagem_url,
                    comunidade_id
                ))

            conexao.commit()
            return comunidade

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


    def apagarComunidade(self, comunidade_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM comunidades
                    WHERE id = %s
                """, (comunidade_id,))

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


    # BUSCAR COMUNIDADES

    def todasComunidades(self, usuario_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT c.*
                    FROM comunidades c
                    LEFT JOIN membros_comunidade mc
                        ON c.id = mc.comunidade_id
                        AND mc.usuario_id = %s
                    WHERE mc.id IS NULL
                """, (usuario_id,))

                return cursor.fetchall()

        finally:
            conexao.close()


    def buscarComunidade(self, comunidade_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT *
                    FROM comunidades
                    WHERE id = %s
                """, (comunidade_id,))

                return cursor.fetchone()

        finally:
            conexao.close()


    def todasComunidadesPorUsuario(self, usuario_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT c.*
                    FROM comunidades c
                    INNER JOIN membros_comunidade mc
                        ON c.id = mc.comunidade_id
                    WHERE mc.usuario_id = %s
                """, (usuario_id,))

                return cursor.fetchall()

        finally:
            conexao.close()


    # FILTRO COMUNIDADE POR GÊNERO

    def comunidadesPorGenero(self, genero):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT *
                    FROM comunidades
                    WHERE genero = %s
                """, (genero,))

                return cursor.fetchall()

        finally:
            conexao.close()


    # ENTRAR E SAIR DA COMUNIDADE

    def entrarComunidade(self, usuario_id, comunidade_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO membros_comunidade
                    (usuario_id, comunidade_id)
                    VALUES (%s, %s)
                """, (usuario_id, comunidade_id))

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


    def sairComunidade(self, usuario_id, comunidade_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM membros_comunidade
                    WHERE usuario_id = %s
                    AND comunidade_id = %s
                """, (usuario_id, comunidade_id))

                removido = cursor.rowcount > 0

            conexao.commit()
            return removido

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


    def usuarioParticipa(self, usuario_id, comunidade_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT id
                    FROM membros_comunidade
                    WHERE usuario_id = %s
                    AND comunidade_id = %s
                """, (usuario_id, comunidade_id))

                resultado = cursor.fetchone()

                return resultado is not None

        finally:
            conexao.close()


    def buscarComunidadesPorNome(self, nome):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT *
                    FROM comunidades
                    WHERE nome ILIKE %s
                """, (f"%{nome}%",))

                return cursor.fetchall()

        finally:
            conexao.close()


    def contarMembros(self, comunidade_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(DISTINCT usuario_id) AS total
                    FROM membros_comunidade
                    WHERE comunidade_id = %s
                """, (comunidade_id,))

                return cursor.fetchone()["total"]

        finally:
            conexao.close()