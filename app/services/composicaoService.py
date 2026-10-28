
from app.models.composicao import Composicao


class ComposicaoService:

    def __init__(self, repoComposicao):
        self.repoComposicao = repoComposicao

    def criar(self, usuario_id, dados):
        titulo = dados.get("titulo", "").strip()
        estilo = dados.get("estilo_musical", "Outro")
        letra = dados.get("letra", "").strip()
        publica = dados.get("publica", False)

        if not isinstance(titulo, str) or not titulo:
            raise ValueError("Informe o título da música.")

        if len(titulo) > 150:
            raise ValueError("O título deve ter até 150 caracteres.")

        if not isinstance(letra, str) or not letra:
            raise ValueError("Informe a letra da música.")

        if len(letra) > 100000:
            raise ValueError("A letra ultrapassou o limite permitido.")

        if not isinstance(estilo, str):
            raise ValueError("Informe um estilo musical válido.")

        estilo = estilo.strip() or "Outro"

        if len(estilo) > 80:
            raise ValueError("O estilo deve ter até 80 caracteres.")

        if not isinstance(publica, bool):
            raise ValueError("Informe uma visibilidade válida.")

        composicao = Composicao(
            usuario_id=usuario_id,
            titulo=titulo,
            estilo_musical=estilo,
            letra=letra,
            publica=publica
        )

        return self.repoComposicao.criar(composicao)

    def listar(self, usuario_id):
        return self.repoComposicao.listarPorUsuario(usuario_id)

    def listarPublicas(self):
        return self.repoComposicao.listarPublicas()

    def buscar(self, composicao_id, usuario_id):
        return self.repoComposicao.buscarPorId(
            composicao_id,
            usuario_id
        )

    def buscarPublica(self, composicao_id):
        return self.repoComposicao.buscarPublicaPorId(composicao_id)

    def atualizar(self, composicao_id, usuario_id, dados):
        titulo = dados.get("titulo", "")
        estilo = dados.get("estilo_musical", "Outro")
        letra = dados.get("letra", "")
        publica = dados.get("publica", False)

        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError("Informe o título da música.")

        if len(titulo.strip()) > 150:
            raise ValueError("O título deve ter até 150 caracteres.")

        if not isinstance(letra, str) or not letra.strip():
            raise ValueError("Informe a letra da música.")

        if len(letra) > 100000:
            raise ValueError("A letra ultrapassou o limite permitido.")

        if not isinstance(estilo, str):
            raise ValueError("Informe um estilo musical válido.")

        estilo = estilo.strip() or "Outro"

        if len(estilo) > 80:
            raise ValueError("O estilo deve ter até 80 caracteres.")

        if not isinstance(publica, bool):
            raise ValueError("Informe uma visibilidade válida.")

        existente = self.buscar(composicao_id, usuario_id)

        if not existente:
            return None

        self.repoComposicao.atualizar(
            composicao_id,
            usuario_id,
            titulo.strip(),
            estilo,
            letra.strip(),
            publica
        )

        return self.buscar(composicao_id, usuario_id)

    def excluir(self, composicao_id, usuario_id):
        existente = self.buscar(composicao_id, usuario_id)

        if not existente:
            return False

        return self.repoComposicao.excluir(
            composicao_id,
            usuario_id
        ) > 0
