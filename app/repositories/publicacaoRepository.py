from database import conectar

class PublicacaoRepository:

    
    def salvarPublicacao(self, publicacao):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO publicacoes
                    (
                        usuario_id,
                        comunidade_id,
                        legenda,
                        imagem_url,
                        tipo_midia,
                        status_moderacao
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    publicacao.usuario_id,
                    publicacao.comunidade_id,
                    publicacao.legenda,
                    publicacao.imagem_url,
                    publicacao.tipo_midia,
                    publicacao.status_moderacao
                ))

                publicacao.id = cursor.fetchone()["id"]

            conexao.commit()
            return publicacao

        except Exception as e:
            conexao.rollback()
            print("Erro ao salvar publicação:", e)
            return "ERRO"

        finally:
            conexao.close()


    # Feed Descobrir
    def carregarPublicacoes(self, usuario_id=None):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        p.*,
                        u.nome AS nome_usuario,
                        u.foto_url,
                        comunidades.nome AS nome_comunidade,

                        (
                            SELECT COUNT(*)
                            FROM curtidas c
                            WHERE c.publicacao_id = p.id
                        ) AS total_curtidas,

                        (
                            SELECT COUNT(*)
                            FROM comentarios co
                            WHERE co.publicacao_id = p.id
                        ) AS total_comentarios,

                        EXISTS (
                            SELECT 1
                            FROM curtidas c2
                            WHERE c2.publicacao_id = p.id
                            AND c2.usuario_id = %s
                        ) AS curtida_usuario

                    FROM publicacoes p

                    JOIN usuarios u
                        ON p.usuario_id = u.id

                    JOIN comunidades
                        ON p.comunidade_id = comunidades.id

                    ORDER BY p.id DESC
                """, (usuario_id,))

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


    # Publicações de uma comunidade
    def carregarPublicacoesPorComunidade(
        self,
        comunidade_id,
        usuario_id=None
    ):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        p.*,
                        u.nome AS nome_usuario,
                        u.foto_url,

                        (
                            SELECT COUNT(*)
                            FROM curtidas c
                            WHERE c.publicacao_id = p.id
                        ) AS total_curtidas,

                        (
                            SELECT COUNT(*)
                            FROM comentarios co
                            WHERE co.publicacao_id = p.id
                        ) AS total_comentarios,

                        EXISTS (
                            SELECT 1
                            FROM curtidas c2
                            WHERE c2.publicacao_id = p.id
                            AND c2.usuario_id = %s
                        ) AS curtida_usuario

                    FROM publicacoes p

                    JOIN usuarios u
                        ON p.usuario_id = u.id

                    WHERE p.comunidade_id = %s

                    ORDER BY p.id DESC
                """, (
                    usuario_id,
                    comunidade_id
                ))

                return cursor.fetchall()

        finally:
            conexao.close()


    # Feed Seguindo
    def listarFeedSeguindo(self, usuario_id):
        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        p.*,
                        u.nome AS nome_usuario,
                        u.foto_url,
                        comunidades.nome AS nome_comunidade,

                        (
                            SELECT COUNT(*)
                            FROM curtidas c
                            WHERE c.publicacao_id = p.id
                        ) AS total_curtidas,

                        (
                            SELECT COUNT(*)
                            FROM comentarios co
                            WHERE co.publicacao_id = p.id
                        ) AS total_comentarios,

                        EXISTS (
                            SELECT 1
                            FROM curtidas c2
                            WHERE c2.publicacao_id = p.id
                            AND c2.usuario_id = %s
                        ) AS curtida_usuario

                    FROM publicacoes p

                    INNER JOIN membros_comunidade mc
                        ON mc.comunidade_id = p.comunidade_id

                    INNER JOIN usuarios u
                        ON u.id = p.usuario_id

                    INNER JOIN comunidades
                        ON comunidades.id = p.comunidade_id

                    WHERE mc.usuario_id = %s

                    ORDER BY p.data_criacao DESC
                """, (
                    usuario_id,
                    usuario_id
                ))

                return cursor.fetchall()

        finally:
            conexao.close()