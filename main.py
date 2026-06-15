import sys

import pygame

from src.jogadores.logica import (
    Jogador,
    decidir_jogador_inicial,
    mover_jogador,
    proximo_jogador,
    rolar_dados,
)
from src.visual.renderizador import (
    FPS,
    DIMENSOES_TELA,
    TITULO_JOGO,
    criar_posicoes_perimetro,
    criar_tabuleiro_exemplo,
    desenhar_jogadores,
    desenhar_painel,
    desenhar_tabuleiro,
)


def main():
    pygame.init()
    tela = pygame.display.set_mode(DIMENSOES_TELA)
    pygame.display.set_caption(TITULO_JOGO)
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 20)

    tabuleiro = criar_tabuleiro_exemplo()
    posicoes_perimetro = criar_posicoes_perimetro()

    jogadores = [
        Jogador("Jogador 1", (255, 200, 40)),
        Jogador("Jogador 2", (180, 80, 255)),
    ]

    sorteio_realizado = False
    mensagem_principal = "Sorteio inicial"
    mensagem_secundaria = "Pressione ESPACO para sortear quem comeca"
    rodando = True

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rodando = False
                elif event.key == pygame.K_SPACE:
                    if not sorteio_realizado:
                        rolagens = []
                        for jogador in jogadores:
                            r = rolar_dados(2)
                            jogador.ultimo_lance = r
                            rolagens.append(r)

                        vez = decidir_jogador_inicial(jogadores)
                        sorteio_realizado = True

                        texto_rolagens = " | ".join(
                            f"{j.nome}: {j.ultimo_lance}" for j in jogadores
                        )
                        mensagem_principal = f"Vez: {jogadores[vez].nome} | {texto_rolagens}"
                        mensagem_secundaria = f"{jogadores[vez].nome} comeca! Pressione ESPACO para rolar 1 dado"
                    else:
                        jogador = jogadores[vez]
                        lance = rolar_dados(1)
                        jogador.ultimo_lance = lance
                        mover_jogador(jogador, lance, len(posicoes_perimetro))

                        mensagem_principal = f"Vez: {jogador.nome} | Ultimo lance: {lance}"
                        mensagem_secundaria = f"{jogador.nome} tirou {lance} e foi para casa {jogador.posicao}"

                        if jogador.posicao == len(posicoes_perimetro) - 1:
                            mensagem_secundaria = f"{jogador.nome} venceu o jogo!"
                        else:
                            vez = proximo_jogador(vez, len(jogadores))
                            mensagem_principal = f"Vez: {jogadores[vez].nome} | Ultimo lance: {jogadores[vez].ultimo_lance}"
                            mensagem_secundaria = f"{jogadores[vez].nome}, pressione ESPACO para rolar 1 dado"

        desenhar_tabuleiro(tela, tabuleiro)
        desenhar_jogadores(tela, jogadores, posicoes_perimetro)
        desenhar_painel(tela, mensagem_principal, mensagem_secundaria, fonte)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
