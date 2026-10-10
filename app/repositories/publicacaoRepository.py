from database import conectar


class PublicacaoRepository:

    def salvarPublicacao(self, publicacao):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO publicacoes
                    (usuario_id, comunidade_id, legenda, imagem_url, status_moderacao)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    publicacao.usuario_id,
                    publicacao.comunidade_id,
                    publicacao.legenda,
                    publicacao.imagem_url,
                    publicacao.status_moderacao
                ))

                publicacao.id = cursor.fetchone()["id"]

            conexao.commit()
            return publicacao

        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()


    def carregarPublicacoes(self):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
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
                    ORDER BY publicacoes.id DESC
                """)

                return cursor.fetchall()
        finally:
            conexao.close()


    def buscarPublicacao(self, publicacao_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT *
                    FROM publicacoes
                    WHERE id = %s
                """, (publicacao_id,))

                return cursor.fetchone()
        finally:
            conexao.close()


    def apagarPublicacao(self, publicacao_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM publicacoes
                    WHERE id = %s
                """, (publicacao_id,))

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()


    def carregarPublicacoesPorComunidade(self, comunidade_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
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
                    WHERE publicacoes.comunidade_id = %s
                    ORDER BY publicacoes.id DESC
                """, (comunidade_id,))

                return cursor.fetchall()
        finally:
            conexao.close()