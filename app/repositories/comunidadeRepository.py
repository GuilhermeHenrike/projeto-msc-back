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

                    AND NOT EXISTS (
                        SELECT 1
                        FROM comunidade_bloqueios cb
                        WHERE cb.comunidade_id = c.id
                        AND cb.usuario_id = %s
                    )
                """, (usuario_id, usuario_id))

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

    # Verificar se o usuário está bloqueado

    def usuarioBloqueado(self, usuario_id, comunidade_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT id
                    FROM comunidade_bloqueios
                    WHERE usuario_id = %s
                    AND comunidade_id = %s
                """, (usuario_id, comunidade_id))


            
            return cursor.fetchone() is not None

        finally:
            conexao.close()

    # Bloquear participante

    def bloquearUsuario(self, comunidade_id, usuario_id, criador_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:

                cursor.execute("""
                    SELECT id
                    FROM membros_comunidade
                    WHERE usuario_id = %s
                    AND comunidade_id = %s
            """, (usuario_id, comunidade_id))

            if cursor.fetchone() is None:
                return False

            cursor.execute("""
                INSERT INTO comunidade_bloqueios
                (comunidade_id, usuario_id, bloqueado_por)
                VALUES (%s, %s, %s)
            """, (comunidade_id, usuario_id, criador_id))

            cursor.execute("""
                DELETE FROM membros_comunidade
                WHERE usuario_id = %s
                AND comunidade_id = %s
            """, (usuario_id, comunidade_id))

            conexao.commit()
            return True

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    # Desbloquear participante

    def desbloquearUsuario(self, comunidade_id, usuario_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                DELETE FROM comunidade_bloqueios
                WHERE comunidade_id = %s
                AND usuario_id = %s
            """, (comunidade_id, usuario_id))

            removido = cursor.rowcount > 0

            conexao.commit()
            return removido

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    # Listar usuários bloqueados

    def listarUsuariosBloqueados(self, comunidade_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        u.id,
                        u.nome,
                        u.foto_url,
                        cb.data_bloqueio
                    FROM comunidade_bloqueios cb
                    INNER JOIN usuarios u
                        ON cb.usuario_id = u.id
                    WHERE cb.comunidade_id = %s
                    ORDER BY cb.data_bloqueio DESC
                """, (comunidade_id,))

                return cursor.fetchall()

        finally:
            conexao.close()

    # Listar participantes atuais
    def listarParticipantes(self, comunidade_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        u.id,
                        u.nome,
                        u.foto_url
                    FROM membros_comunidade mc
                    INNER JOIN usuarios u
                        ON mc.usuario_id = u.id
                    WHERE mc.comunidade_id = %s
                    AND u.id <> (
                        SELECT criador_id
                        FROM comunidades
                        WHERE id = %s
                    )
                    ORDER BY u.nome
                """, (comunidade_id,))

                return cursor.fetchall()

        finally:
            conexao.close()