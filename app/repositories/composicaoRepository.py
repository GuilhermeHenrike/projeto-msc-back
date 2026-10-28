
from database import conectar


class ComposicaoRepository:

    def criar(self, composicao):
        conexao = conectar()

        try:
            cursor = conexao.cursor()

            sql = """
                INSERT INTO composicoes
                (usuario_id, titulo, estilo_musical, letra, publica)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                composicao.usuario_id,
                composicao.titulo,
                composicao.estilo_musical,
                composicao.letra,
                composicao.publica
            ))

            composicao_id = cursor.lastrowid
            conexao.commit()

            return self.buscarPorId(
                composicao_id,
                composicao.usuario_id
            )

        except Exception:
            conexao.rollback()
            raise

        finally:
            if 'cursor' in locals():
                cursor.close()
            conexao.close()

    def listarPorUsuario(self, usuario_id):
        conexao = conectar()

        try:
            cursor = conexao.cursor(dictionary=True)

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
            if 'cursor' in locals():
                cursor.close()
            conexao.close()

    def buscarPorId(self, composicao_id, usuario_id):
        conexao = conectar()

        try:
            cursor = conexao.cursor(dictionary=True)

            sql = """
                SELECT id, usuario_id, titulo, estilo_musical,
                       letra, publica, data_criacao, data_atualizacao
                FROM composicoes
                WHERE id = %s AND usuario_id = %s
            """

            cursor.execute(sql, (composicao_id, usuario_id))
            return cursor.fetchone()

        finally:
            if 'cursor' in locals():
                cursor.close()
            conexao.close()

    def listarPublicas(self):
        conexao = conectar()

        try:
            cursor = conexao.cursor(dictionary=True)

            sql = """
                SELECT id, titulo, estilo_musical, letra
                FROM composicoes
                WHERE publica = TRUE
                ORDER BY data_atualizacao DESC
            """

            cursor.execute(sql)
            return cursor.fetchall()

        finally:
            if 'cursor' in locals():
                cursor.close()
            conexao.close()

    def buscarPublicaPorId(self, composicao_id):
        conexao = conectar()

        try:
            cursor = conexao.cursor(dictionary=True)

            sql = """
                SELECT id, titulo, estilo_musical, letra
                FROM composicoes
                WHERE id = %s AND publica = TRUE
            """

            cursor.execute(sql, (composicao_id,))
            return cursor.fetchone()

        finally:
            if 'cursor' in locals():
                cursor.close()
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
            cursor = conexao.cursor()

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
            if 'cursor' in locals():
                cursor.close()
            conexao.close()

    def excluir(self, composicao_id, usuario_id):
        conexao = conectar()

        try:
            cursor = conexao.cursor()

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
            if 'cursor' in locals():
                cursor.close()
            conexao.close()
