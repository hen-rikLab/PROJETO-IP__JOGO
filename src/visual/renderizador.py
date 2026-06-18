import pygame

# Titulo da janela do jogo
TITULO_JOGO = "The Maze Runner"
# Quantidade de quadros por segundo
FPS = 30

# Tamanho de cada casa do tabuleiro
TAMANHO_CELULA = 60
# Espacamento entre as casas
MARGEM = 5
# Quantidade de colunas do tabuleiro
COLUNAS = 10
# Quantidade de linhas do tabuleiro
LINHAS = 7
# Altura reservada para o painel inferior
ALTURA_PAINEL = 140

# Largura total da area do tabuleiro
LARGURA_TABULEIRO = COLUNAS * (TAMANHO_CELULA + MARGEM) + MARGEM
# Altura total da area do tabuleiro
ALTURA_TABULEIRO = LINHAS * (TAMANHO_CELULA + MARGEM) + MARGEM
# Dimensoes finais da janela do jogo
DIMENSOES_TELA = (LARGURA_TABULEIRO, ALTURA_TABULEIRO + ALTURA_PAINEL)

# Cor de fundo geral da tela
COR_FUNDO = (30, 30, 30)
# Cor base da area do tabuleiro
COR_TABULEIRO = (30, 30, 30)
# Cor do painel inferior
COR_PAINEL = (40, 40, 40)
# Cor das bordas das casas do tabuleiro
COR_BORDA = (50, 50, 50)

# Cores usadas para pintar cada tipo de casa do tabuleiro
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
    """Monta a ordem das casas que formam o contorno do tabuleiro."""
    posicoes = []

    # Percorre a primeira linha da esquerda para a direita
    for coluna in range(COLUNAS):
        posicoes.append(coluna)

    # Percorre a lateral direita de cima para baixo, sem repetir cantos
    for linha in range(1, LINHAS - 1):
        posicoes.append(linha * COLUNAS + (COLUNAS - 1))

    # Percorre a ultima linha da direita para a esquerda
    for coluna in range(COLUNAS - 1, -1, -1):
        posicoes.append((LINHAS - 1) * COLUNAS + coluna)

    # Percorre a lateral esquerda de baixo para cima, pulando linhas internas repetidas
    for linha in range(LINHAS - 2, 0, -1):
        if linha == 1 or linha == 2:
            continue
        posicoes.append(linha * COLUNAS)

    return posicoes


def criar_tabuleiro_exemplo():
    """Cria um tabuleiro simples com cores distribuidas no perimetro."""
    # Inicializa todas as casas como vazias
    tabuleiro = [None] * (LINHAS * COLUNAS)

    # Sequencia de tipos que sera repetida ao longo do perimetro
    tipos_perimetro = [
        "start", "white", "red", "green", "white", "blue", "white", "yellow", "white", "red",
        "green", "black", "blue", "white", "white", "red", "green", "white", "yellow", "white",
        "red", "green", "white", "blue", "red", "yellow", "green", "end",
    ]

    posicoes_perimetro = criar_posicoes_perimetro()

    # Preenche apenas as casas do contorno com as cores da lista
    indice_tipo = 0
    for posicao_tabuleiro in posicoes_perimetro:
        tabuleiro[posicao_tabuleiro] = tipos_perimetro[indice_tipo]
        indice_tipo += 1
        if indice_tipo == len(tipos_perimetro):
            indice_tipo = 0

    return tabuleiro


def desenhar_tabuleiro(tela, tabuleiro):
    """Desenha o fundo do tabuleiro e pinta cada casa conforme o tipo."""
    # Limpa a tela com a cor de fundo geral
    tela.fill(COR_FUNDO)

    # Desenha a area principal do tabuleiro
    retangulo_tabuleiro = pygame.Rect(0, 0, DIMENSOES_TELA[0], ALTURA_TABULEIRO)
    pygame.draw.rect(tela, COR_TABULEIRO, retangulo_tabuleiro)

    # Percorre todas as casas do tabuleiro para pintar uma por uma
    for indice, tipo_celula in enumerate(tabuleiro):
        # Converte o indice linear para linha e coluna
        linha = indice // COLUNAS
        coluna = indice % COLUNAS
        # Calcula a posicao real da casa na tela
        x = MARGEM + coluna * (TAMANHO_CELULA + MARGEM)
        y = MARGEM + linha * (TAMANHO_CELULA + MARGEM)
        retangulo_celula = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)

        # Casas vazias ficam apenas em tom escuro
        if tipo_celula is None:
            pygame.draw.rect(tela, (20, 20, 20), retangulo_celula)
            continue

        # Busca a cor correspondente ao tipo da casa
        cor = CORES_CELULA.get(tipo_celula, (200, 200, 200))
        pygame.draw.rect(tela, cor, retangulo_celula)
        pygame.draw.rect(tela, COR_BORDA, retangulo_celula, 2)


def desenhar_jogadores(tela, jogadores, posicoes_perimetro):
    """Desenha os jogadores como circulos sobre as casas do perimetro."""
    # Percorre todos os jogadores ativos
    for indice, jogador in enumerate(jogadores):
        # Garante que a posicao usada para o desenho nao saia do intervalo valido
        posicao_segura = jogador.posicao
        if posicao_segura < 0:
            posicao_segura = 0
        if posicao_segura >= len(posicoes_perimetro):
            posicao_segura = len(posicoes_perimetro) - 1

        # Descobre qual indice do tabuleiro corresponde a posicao do perimetro
        indice_tabuleiro = posicoes_perimetro[posicao_segura]
        linha = indice_tabuleiro // COLUNAS
        coluna = indice_tabuleiro % COLUNAS
        x = MARGEM + coluna * (TAMANHO_CELULA + MARGEM)
        y = MARGEM + linha * (TAMANHO_CELULA + MARGEM)

        # Pequenos deslocamentos para os dois circulos nao ficarem exatamente sobrepostos
        deslocamento_x = 10 if indice == 0 else 30
        deslocamento_y = 30
        centro = (x + deslocamento_x, y + deslocamento_y)

        # Desenha o jogador com a cor definida no objeto
        pygame.draw.circle(tela, jogador.cor, centro, 10)


def desenhar_painel(tela, mensagem_principal, mensagem_secundaria, fonte):
    """Desenha o painel inferior com as mensagens do jogo."""
    # Calcula a coordenada inicial do painel na parte de baixo da tela
    y_painel = ALTURA_TABULEIRO + MARGEM
    pygame.draw.rect(tela, COR_PAINEL, (0, y_painel, DIMENSOES_TELA[0], ALTURA_PAINEL))

    # Renderiza as duas linhas de texto exibidas no painel
    texto_principal = fonte.render(mensagem_principal, True, (230, 230, 230))
    texto_secundario = fonte.render(mensagem_secundaria, True, (200, 200, 200))

    # Posiciona os textos com uma pequena margem interna
    tela.blit(texto_principal, (10, y_painel + 18))
    tela.blit(texto_secundario, (10, y_painel + 48))