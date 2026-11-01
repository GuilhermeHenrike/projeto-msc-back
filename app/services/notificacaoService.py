class NotificacaoService:

    def __init__(self, notificacaoRepository):
        self.notificacaoRepository = notificacaoRepository

    def notificarInteracao(self, usuario_origem_id, publicacao_id, tipo):

        if tipo not in ["curtida", "comentario"]:
            return

        dono_publicacao = (
            self.notificacaoRepository.buscarDonoPublicacao(publicacao_id)
        )

        # Não notificar o próprio autor
        if dono_publicacao is None or dono_publicacao == usuario_origem_id:
            return

        self.notificacaoRepository.criarNotificacao(
            usuario_destino_id=dono_publicacao,
            usuario_origem_id=usuario_origem_id,
            tipo=tipo,
            publicacao_id=publicacao_id
        )

    def listarNotificacoes(self, usuario_id):

        return self.notificacaoRepository.listarNotificacoes(usuario_id)