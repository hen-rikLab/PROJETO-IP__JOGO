import sys

import pygame

# Importa as classes e funcoes da logica do jogo
from src.jogadores.logica import (  # noqa: E501
    Jogador,  # classe que representa cada jogador
    decidir_jogador_inicial,  # sorteia quem comeca (2 dados cada)
    mover_jogador,  # avanca o jogador no perimetro
    proximo_jogador,  # alterna para o proximo jogador
    rolar_dados,  # rola N dados de 1 a 6
)
# Importa as funcoes de desenho da tela
from src.visual.renderizador import (  # noqa: E501
    FPS,  # taxa de quadros por segundo
    DIMENSOES_TELA,  # largura e altura da janela
    TITULO_JOGO,  # titulo da janela
    criar_posicoes_perimetro,  # gera a ordem das casas no perimetro
    criar_tabuleiro_exemplo,  # cria o tabuleiro com as cores das casas
    desenhar_jogadores,  # desenha os circulos dos jogadores
    desenhar_painel,  # desenha o painel inferior com mensagens
    desenhar_tabuleiro,  # desenha a grade do tabuleiro
)


def main():
    """Laco principal do jogo: inicializa pygame, gerencia eventos e atualiza a tela."""
    # Inicializa o pygame e cria a janela
    pygame.init()
    tela = pygame.display.set_mode(DIMENSOES_TELA)
    pygame.display.set_caption(TITULO_JOGO)
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 20)

    # Cria o tabuleiro e a lista de posicoes do perimetro
    tabuleiro = criar_tabuleiro_exemplo()
    posicoes_perimetro = criar_posicoes_perimetro()

    # Cria os dois jogadores com nome e cor (RGB)
    jogadores = [
        Jogador("Jogador 1", (255, 200, 40)),
        Jogador("Jogador 2", (180, 80, 255)),
    ]

    # Controle de estado do jogo
    sorteio_realizado = False  # True depois que o sorteio inicial for feito
    mensagem_principal = "Sorteio inicial"  # linha de cima do painel
    mensagem_secundaria = "Pressione ESPACO para sortear quem comeca"  # linha de baixo
    rodando = True  # False quando o jogador fechar o jogo

    while rodando:
        # Processa todos os eventos ocorridos desde o ultimo frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rodando = False
                elif event.key == pygame.K_SPACE:

                    # --- SORTEIO INICIAL (primeiro ESPACO) ---
                    # Requisito: "rolar 2 dados deve ser apenas para
                    # escolher quem vai comecar jogando"
                    # Implementacao: na primeira vez que ESPACO e
                    # pressionado, cada jogador rola 2 dados.
                    # O resultado define quem comeca.
                    if not sorteio_realizado:
                        vez, rolagens = decidir_jogador_inicial(jogadores)
                        for i, jogador in enumerate(jogadores):
                            jogador.ultimo_lance = rolagens[i]
                        sorteio_realizado = True

                        # Mostra o resultado do sorteio no painel
                        texto_rolagens = " | ".join(
                            f"{j.nome}: {j.ultimo_lance}" for j in jogadores
                        )
                        mensagem_principal = f"Vez: {jogadores[vez].nome} | {texto_rolagens}"
                        mensagem_secundaria = f"{jogadores[vez].nome} comeca! Pressione ESPACO para rolar 1 dado"

                    # --- JOGADA NORMAL (proximos ESPACOS) ---
                    # Requisito: "cada jogador ira rolar 1 dado por vez
                    # e andar as respectivas casas"
                    # Implementacao: apos o sorteio, cada vez que ESPACO
                    # e pressionado o jogador da vez rola 1 dado
                    # (rolar_dados(1)) e avanca esse numero de casas.
                    else:
                        jogador = jogadores[vez]
                        lance = rolar_dados(1)  # rola 1 dado (valor 1 a 6)
                        jogador.ultimo_lance = lance
                        mover_jogador(jogador, lance, len(posicoes_perimetro))

                        # Atualiza o painel com o resultado da jogada
                        mensagem_principal = f"Vez: {jogador.nome} | Ultimo lance: {lance}"
                        mensagem_secundaria = f"{jogador.nome} tirou {lance} e foi para casa {jogador.posicao}"

                        # Verifica se o jogador chegou ao final do perimetro
                        if jogador.posicao == len(posicoes_perimetro) - 1:
                            mensagem_secundaria = f"{jogador.nome} venceu o jogo!"
                        else:
                            # Passa a vez para o proximo jogador
                            vez = proximo_jogador(vez, len(jogadores))
                            mensagem_principal = f"Vez: {jogadores[vez].nome} | Ultimo lance: {jogadores[vez].ultimo_lance}"
                            mensagem_secundaria = f"{jogadores[vez].nome}, pressione ESPACO para rolar 1 dado"

        # --- RENDERIZACAO ---
        desenhar_tabuleiro(tela, tabuleiro)
        desenhar_jogadores(tela, jogadores, posicoes_perimetro)
        desenhar_painel(tela, mensagem_principal, mensagem_secundaria, fonte)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
