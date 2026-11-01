from database import conectar

class ComposicaoRepository:

    def criar(self, composicao):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    INSERT INTO composicoes
                    (usuario_id, titulo, estilo_musical, letra, publica)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """

                cursor.execute(sql, (
                    composicao.usuario_id,
                    composicao.titulo,
                    composicao.estilo_musical,
                    composicao.letra,
                    composicao.publica
                ))

                composicao_id = cursor.fetchone()["id"]

            conexao.commit()

            return self.buscarPorId(
                composicao_id,
                composicao.usuario_id
            )

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


    def listarPorUsuario(self, usuario_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    SELECT id, usuario_id, titulo, estilo_musical,
                        letra, publica, data_criacao, data_atualizacao
                    FROM composicoes
                    WHERE usuario_id = %s
                    ORDER BY data_atualizacao DESC
                """

                cursor.execute(sql, (usuario_id,))
                return cursor.fetchall()

        finally:
            conexao.close()


    def buscarPorId(self, composicao_id, usuario_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    SELECT id, usuario_id, titulo, estilo_musical,
                        letra, publica, data_criacao, data_atualizacao
                    FROM composicoes
                    WHERE id = %s AND usuario_id = %s
                """

                cursor.execute(sql, (composicao_id, usuario_id))
                return cursor.fetchone()

        finally:
            conexao.close()


    def listarPublicas(self):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    SELECT
                        c.id,
                        c.usuario_id,
                        c.titulo,
                        c.estilo_musical,
                        c.letra,
                        u.nome AS autor_nome,
                        u.foto_url AS autor_foto_url
                    FROM composicoes c
                    INNER JOIN usuarios u
                        ON c.usuario_id = u.id
                    WHERE c.publica = TRUE
                    ORDER BY c.data_atualizacao DESC
                """

                cursor.execute(sql)
                return cursor.fetchall()

        finally:
            conexao.close()


    def buscarPublicaPorId(self, composicao_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    SELECT
                        c.id,
                        c.usuario_id,
                        c.titulo,
                        c.estilo_musical,
                        c.letra,
                        u.nome AS autor_nome,
                        u.foto_url AS autor_foto_url
                    FROM composicoes c
                    INNER JOIN usuarios u
                        ON c.usuario_id = u.id
                    WHERE c.id = %s
                    AND c.publica = TRUE
                """

                cursor.execute(sql, (composicao_id,))
                return cursor.fetchone()

        finally:
            conexao.close()


    def atualizar(
        self,
        composicao_id,
        usuario_id,
        titulo,
        estilo_musical,
        letra,
        publica
    ):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    UPDATE composicoes
                    SET titulo = %s,
                        estilo_musical = %s,
                        letra = %s,
                        publica = %s
                    WHERE id = %s AND usuario_id = %s
                """

                cursor.execute(sql, (
                    titulo,
                    estilo_musical,
                    letra,
                    publica,
                    composicao_id,
                    usuario_id
                ))

                alteradas = cursor.rowcount

            conexao.commit()
            return alteradas

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


    def excluir(self, composicao_id, usuario_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    DELETE FROM composicoes
                    WHERE id = %s AND usuario_id = %s
                """

                cursor.execute(sql, (composicao_id, usuario_id))

                excluidas = cursor.rowcount

            conexao.commit()
            return excluidas

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()