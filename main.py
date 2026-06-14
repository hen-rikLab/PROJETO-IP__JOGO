import sys

import pygame

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


class Jogador:
    def __init__(self, nome, cor, posicao):
        self.nome = nome
        self.cor = cor
        self.posicao = posicao


def main():
    pygame.init()
    tela = pygame.display.set_mode(DIMENSOES_TELA)
    pygame.display.set_caption(TITULO_JOGO)
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 20)

    tabuleiro = criar_tabuleiro_exemplo()
    posicoes_perimetro = criar_posicoes_perimetro()
    jogadores = [
        Jogador("Jogador 1", (255, 200, 40), 0),
        Jogador("Jogador 2", (180, 80, 255), 0),
    ]
    mensagem_principal = "Vez: Jogador 1 | Ultimo lance: 0"
    mensagem_secundaria = "Jogador 1, pressione ESPACO para rolar 2 dados"
    rodando = True

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rodando = False

        desenhar_tabuleiro(tela, tabuleiro)
        desenhar_jogadores(tela, jogadores, posicoes_perimetro)
        desenhar_painel(tela, mensagem_principal, mensagem_secundaria, fonte)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()