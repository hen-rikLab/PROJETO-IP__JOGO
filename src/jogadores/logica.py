import random


class Jogador:
    """Representa um jogador no jogo.
    - nome: identificacao do jogador
    - cor: cor do circulo no tabuleiro (RGB)
    - posicao: casa atual no perimetro
    - ultimo_lance: valor do ultimo dado rolado
    - rodadas_sem_jogar: quantas rodadas o jogador ficou sem jogar
    - life: vida atual do jogador
    - skip_turn: indica se o jogador deve pular a proxima vez
    """
    def __init__(self, nome, cor):
        self.nome = nome
        self.cor = cor
        self.posicao = 0
        self.ultimo_lance = 0
        self.rodadas_sem_jogar = 0
        self.life = 10
        self.skip_turn = False

    def resetar(self):
        """Volta todas as propriedades ao estado inicial."""
        self.posicao = 0
        self.ultimo_lance = 0
        self.rodadas_sem_jogar = 0
        self.life = 10
        self.skip_turn = False


def rolar_dados(quantidade=2):
    """
    Requisito: "cada dado rolado so pode ir de 1 a 6"
    Implementacao: usa random.randint(1, 6) para garantir
    que cada dado individual gere valores exclusivamente de 1 a 6.
    O parametro `quantidade` controla quantos dados sao somados.
    """
    total = 0
    for _ in range(quantidade):
        total += random.randint(1, 6)
    return total


def mover_jogador(jogador, passos, tamanho_perimetro):
    """Avanca o `jogador` em `passos` casas no perimetro.
    - Se ultrapassar a ultima casa, trava nela.
    - Retorna a nova posicao.
    """
    nova_pos = jogador.posicao + passos
    jogador.posicao = min(nova_pos, tamanho_perimetro - 1) # garante que o jogador nao ultrapasse a ultima casa
    return jogador.posicao


def decidir_jogador_inicial(jogadores):
    """
    Requisito: "a funcao de rolar 2 dados deve ser apenas para escolher
    quem vai comecar jogando"
    Implementacao: cada jogador rola 2 dados (rolar_dados(2)).
    Quem tirar a maior soma comeca. Em caso de empate, todos
    rolam novamente ate haver um vencedor unico.
    Retorna (indice_vencedor, lista_rolagens) — as rolagens retornadas
    sao exatamente as mesmas usadas para decidir o vencedor.
    """
    while True:
        rolagens = [rolar_dados(2) for _ in jogadores]
        max_val = max(rolagens)
        if rolagens.count(max_val) == 1:
            return rolagens.index(max_val), rolagens


def proximo_jogador(vez_atual, total_jogadores):
    """Retorna o indice do proximo jogador na ordem circular."""
    return (vez_atual + 1) % total_jogadores
