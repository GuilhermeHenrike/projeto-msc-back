class CurtidaService:

    def __init__(self, curtidaRepository):
        self.curtidaRepository = curtidaRepository


    def curtir(self, usuario_id, publicacao_id):

        curtida = self.curtidaRepository.verificarCurtida(usuario_id, publicacao_id )

        if curtida:
            self.curtidaRepository.descurtir(usuario_id, publicacao_id)

            return False

        self.curtidaRepository.curtir(usuario_id, publicacao_id)

        return True

    def contarCurtidas(self, publicacao_id):

        return self.curtidaRepository.contarCurtidas(publicacao_id)