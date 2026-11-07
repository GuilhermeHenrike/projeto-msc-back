
from app.models.composicao import Composicao
from app.services.moderacaoService import moderarComposicao


class ComposicaoService:

    def __init__(self, repoComposicao):
        self.repoComposicao = repoComposicao

    def _validar_moderacao(self, titulo, estilo, letra):
        try:
            aprovado = moderarComposicao(
                titulo,
                estilo,
                letra
            )

        except Exception as erro:
            raise RuntimeError(
                "Não foi possível analisar a composição. Tente novamente."
            ) from erro

        if not aprovado:
            raise ValueError(
                "Sua composição contém conteúdo não permitido pela plataforma."
            )

    def criar(self, usuario_id, dados):
        titulo = dados.get("titulo", "")
        estilo = dados.get("estilo_musical", "Outro")
        letra = dados.get("letra", "")
        publica = dados.get("publica", False)

        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError("Informe o título da música.")

        titulo = titulo.strip()

        if len(titulo) > 150:
            raise ValueError("O título deve ter até 150 caracteres.")

        if not isinstance(letra, str) or not letra.strip():
            raise ValueError("Informe a letra da música.")

        letra = letra.strip()

        if len(letra) > 100000:
            raise ValueError("A letra ultrapassou o limite permitido.")

        if not isinstance(estilo, str):
            raise ValueError("Informe um estilo musical válido.")

        estilo = estilo.strip() or "Outro"

        if len(estilo) > 80:
            raise ValueError("O estilo deve ter até 80 caracteres.")

        if not isinstance(publica, bool):
            raise ValueError("Informe uma visibilidade válida.")

        self._validar_moderacao(
            titulo,
            estilo,
            letra
        )

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

        titulo = titulo.strip()

        if len(titulo) > 150:
            raise ValueError("O título deve ter até 150 caracteres.")

        if not isinstance(letra, str) or not letra.strip():
            raise ValueError("Informe a letra da música.")

        letra = letra.strip()

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

        self._validar_moderacao(
            titulo,
            estilo,
            letra
        )

        self.repoComposicao.atualizar(
            composicao_id,
            usuario_id,
            titulo,
            estilo,
            letra,
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
