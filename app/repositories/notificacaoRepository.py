from database import conectar


class NotificacaoRepository:

    def criarNotificacao(self, usuario_destino_id, usuario_origem_id,
                         tipo, publicacao_id=None):

        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO notificacoes
                    (usuario_destino_id, usuario_origem_id, tipo, publicacao_id)
                    VALUES (%s, %s, %s, %s)
                """, (
                    usuario_destino_id,
                    usuario_origem_id,
                    tipo,
                    publicacao_id
                ))

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    def buscarDonoPublicacao(self, publicacao_id):

        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT usuario_id
                    FROM publicacoes
                    WHERE id = %s
                """, (publicacao_id,))

                resultado = cursor.fetchone()

                return resultado["usuario_id"] if resultado else None

        finally:
            conexao.close()

    def listarNotificacoes(self, usuario_id):

        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        n.id,
                        n.tipo,
                        n.publicacao_id,
                        n.data_criacao,
                        u.id AS usuario_origem_id,
                        u.nome AS nome_usuario,
                        u.foto_url,
                        p.legenda
                    FROM notificacoes n
                    INNER JOIN usuarios u
                        ON n.usuario_origem_id = u.id
                    LEFT JOIN publicacoes p
                        ON n.publicacao_id = p.id
                    WHERE n.usuario_destino_id = %s
                    ORDER BY n.data_criacao DESC
                """, (usuario_id,))

                return cursor.fetchall()

        finally:
            conexao.close()