import pygame

TITULO_JOGO = "The Maze Runner"
FPS = 30

TAMANHO_CELULA = 60
MARGEM = 5
COLUNAS = 10
LINHAS = 7
ALTURA_PAINEL = 140

LARGURA_TABULEIRO = COLUNAS * (TAMANHO_CELULA + MARGEM) + MARGEM
ALTURA_TABULEIRO = LINHAS * (TAMANHO_CELULA + MARGEM) + MARGEM
DIMENSOES_TELA = (LARGURA_TABULEIRO, ALTURA_TABULEIRO + ALTURA_PAINEL)

COR_FUNDO = (30, 30, 30)
COR_TABULEIRO = (30, 30, 30)
COR_PAINEL = (40, 40, 40)
COR_BORDA = (50, 50, 50)

CORES_CELULA = {
    "start": (30, 30, 30),
    "end": (30, 30, 30),
    "white": (245, 245, 245),
    "red": (220, 50, 50),
    "green": (50, 200, 50),
    "yellow": (240, 220, 70),
    "blue": (80, 140, 240),
    "black": (30, 30, 30),
}


def criar_posicoes_perimetro():
    posicoes = []

    for coluna in range(COLUNAS):
        posicoes.append(coluna)

    for linha in range(1, LINHAS - 1):
        posicoes.append(linha * COLUNAS + (COLUNAS - 1))

    for coluna in range(COLUNAS - 1, -1, -1):
        posicoes.append((LINHAS - 1) * COLUNAS + coluna)

    for linha in range(LINHAS - 2, 0, -1):
        if linha == 1 or linha == 2:
            continue
        posicoes.append(linha * COLUNAS)

    return posicoes


def criar_tabuleiro_exemplo():
    tabuleiro = [None] * (LINHAS * COLUNAS)

    tipos_perimetro = [
        "start", "white", "red", "green", "white", "blue", "white", "yellow", "white", "red",
        "green", "black", "blue", "white", "white", "red", "green", "white", "yellow", "white",
        "red", "green", "white", "blue", "red", "yellow", "green", "end",
    ]

    posicoes_perimetro = criar_posicoes_perimetro()

    indice_tipo = 0
    for posicao_tabuleiro in posicoes_perimetro:
        tabuleiro[posicao_tabuleiro] = tipos_perimetro[indice_tipo]
        indice_tipo += 1
        if indice_tipo == len(tipos_perimetro):
            indice_tipo = 0

    return tabuleiro


def desenhar_tabuleiro(tela, tabuleiro):
    tela.fill(COR_FUNDO)

    retangulo_tabuleiro = pygame.Rect(0, 0, DIMENSOES_TELA[0], ALTURA_TABULEIRO)
    pygame.draw.rect(tela, COR_TABULEIRO, retangulo_tabuleiro)

    for indice, tipo_celula in enumerate(tabuleiro):
        linha = indice // COLUNAS
        coluna = indice % COLUNAS
        x = MARGEM + coluna * (TAMANHO_CELULA + MARGEM)
        y = MARGEM + linha * (TAMANHO_CELULA + MARGEM)
        retangulo_celula = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)

        if tipo_celula is None:
            pygame.draw.rect(tela, (20, 20, 20), retangulo_celula)
            continue

        cor = CORES_CELULA.get(tipo_celula, (200, 200, 200))
        pygame.draw.rect(tela, cor, retangulo_celula)
        pygame.draw.rect(tela, COR_BORDA, retangulo_celula, 2)


def desenhar_jogadores(tela, jogadores, posicoes_perimetro):
    for indice, jogador in enumerate(jogadores):
        posicao_segura = jogador.posicao
        if posicao_segura < 0:
            posicao_segura = 0
        if posicao_segura >= len(posicoes_perimetro):
            posicao_segura = len(posicoes_perimetro) - 1

        indice_tabuleiro = posicoes_perimetro[posicao_segura]
        linha = indice_tabuleiro // COLUNAS
        coluna = indice_tabuleiro % COLUNAS
        x = MARGEM + coluna * (TAMANHO_CELULA + MARGEM)
        y = MARGEM + linha * (TAMANHO_CELULA + MARGEM)

        deslocamento_x = 10 if indice == 0 else 30
        deslocamento_y = 30
        centro = (x + deslocamento_x, y + deslocamento_y)

        pygame.draw.circle(tela, jogador.cor, centro, 10)


def desenhar_painel(tela, mensagem_principal, mensagem_secundaria, fonte):
    y_painel = ALTURA_TABULEIRO + MARGEM
    pygame.draw.rect(tela, COR_PAINEL, (0, y_painel, DIMENSOES_TELA[0], ALTURA_PAINEL))

    texto_principal = fonte.render(mensagem_principal, True, (230, 230, 230))
    texto_secundario = fonte.render(mensagem_secundaria, True, (200, 200, 200))

    tela.blit(texto_principal, (10, y_painel + 18))
    tela.blit(texto_secundario, (10, y_painel + 48))