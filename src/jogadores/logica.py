import random


class Jogador:
    def __init__(self, nome, cor):
        self.nome = nome
        self.cor = cor
        self.posicao = 0
        self.ultimo_lance = 0
        self.rodadas_sem_jogar = 0

    def resetar(self):
        self.posicao = 0
        self.ultimo_lance = 0
        self.rodadas_sem_jogar = 0


def rolar_dados(quantidade=2):
    total = 0
    for _ in range(quantidade):
        total += random.randint(1, 6)
    return total


def mover_jogador(jogador, passos, tamanho_perimetro):
    nova_pos = jogador.posicao + passos
    jogador.posicao = min(nova_pos, tamanho_perimetro - 1)
    return jogador.posicao


def decidir_jogador_inicial(jogadores):
    while True:
        rolagens = [rolar_dados(2) for _ in jogadores]
        max_val = max(rolagens)
        if rolagens.count(max_val) == 1:
            return rolagens.index(max_val)


def proximo_jogador(vez_atual, total_jogadores):
    return (vez_atual + 1) % total_jogadores
