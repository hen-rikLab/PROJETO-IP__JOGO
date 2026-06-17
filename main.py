import sys
import pygame
import random

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

# --- FUNÇÕES E CLASSES DE APOIO ---

def roll_die():
    """Retorna um valor aleatório de 1 a 6 para o dado."""
    return random.randint(1, 6)

def move_player(current_pos, roll, perimeter_length):
    """Calcula a nova posição do jogador."""
    return current_pos + roll

class Scene:
    """Classe criada para espelhar a estrutura exigida pelo Código 1."""
    def __init__(self, players, board, perimeter_positions):
        self.players = players
        self.current_idx = 0
        self.last_roll = 0
        self.board = board
        self.perimeter_positions = perimeter_positions
        self.message = ""

# --- ADAPTAÇÃO DA CLASSE JOGADOR ---

class Jogador:
    def __init__(self, nome, cor, posicao):
        self.nome = nome 
        self.cor = cor
        self.posicao = posicao
        
        self.pos = posicao 
        self.life = 10     
        self.skip_turn = False


def main():
    pygame.init()
    tela = pygame.display.set_mode(DIMENSOES_TELA)
    pygame.display.set_caption(TITULO_JOGO)
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 20)

    tabuleiro = criar_tabuleiro_exemplo()
    posicoes_perimetro = criar_posicoes_perimetro()
    perimeter_length = len(posicoes_perimetro)

    jogadores = [
        Jogador("Jogador 1", (255, 200, 40), 0),
        Jogador("Jogador 2", (180, 80, 255), 0),
    ]
    
    scene = Scene(jogadores, tabuleiro, posicoes_perimetro)
    phase = "roll"

    rodando = True

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rodando = False
                elif event.key == pygame.K_SPACE:
                    if phase == "roll":
                        player = scene.players[scene.current_idx]
                        
                        # VERIFICAÇÃO DA CASA AMARELA
                        if hasattr(player, 'skip_turn') and player.skip_turn:
                            scene.message = f"{player.name} perdeu a vez (Casa Amarela)!"
                            player.skip_turn = False 
                            phase = "next"
                        
                        # SE O JOGADOR NÃO ESTIVER PRESO
                        else:
                            # Rola o dado e guarda o valor que saiu
                            scene.last_roll = roll_die()
                            # Move o jogador no tabuleiro de acordo com o valor do dado
                            player.pos = move_player(player.pos, scene.last_roll, perimeter_length)
                            # Se o jogador não tem a variável de pular turno
                            if not hasattr(player, 'skip_turn'):
                                player.skip_turn = False

                            # --- REQUISITO 4: AÇÕES DAS CASAS ---
                            
                            # Matemática para converter os "passos" na posição real do mapa
                            safe_position = max(0, min(player.pos, len(scene.perimeter_positions) - 1))
                            board_index = scene.perimeter_positions[safe_position]
                            
                            # Pega a cor que define a casa atual
                            cor_casa = scene.board[board_index]
                            
                            # SE a cor da casa for Vermelha ("red"):
                            if cor_casa == "red":
                                # Tira 3 de vida
                                player.life -= 3
                                # Avisa o que aconteceu
                                scene.message = f"{player.name} tirou {scene.last_roll}, caiu na VERMELHA! (-3) Vida: {player.life}"
                                # Muda a fase para passar o turno
                                phase = "next"
                                
                            # SENÃO, SE a cor da casa for Verde ("green"):
                            elif cor_casa == "green":
                                # Dá 1 de vida
                                player.life += 1
                                # Regra: A vida nao pode passar de 10
                                if player.life > 10: 
                                    player.life = 10
                                # Avisa no painel
                                scene.message = f"{player.name} tirou {scene.last_roll}, caiu na VERDE! (+1) Vida: {player.life}"
                                phase = "next"
                                
                            # SENÃO, SE a cor da casa for Amarela ("yellow"):
                            elif cor_casa == "yellow":
                                # Ativa a armadilha: ele vai pular o próximo turno dele
                                player.skip_turn = True
                                scene.message = f"{player.name} tirou {scene.last_roll}, caiu na AMARELA! Fica preso."
                                phase = "next"
                                
                            # SENÃO, SE a cor da casa for Azul ("blue"):
                            elif cor_casa == "blue":
                                scene.message = f"{player.name} tirou {scene.last_roll}, caiu na AZUL! Joga de novo!"
                                # ATENÇÃO: A fase continua "roll", então o turno não passa. Ele joga de novo!
                                phase = "roll" 
                                
                            # SENÃO, SE a cor da casa for Preta ("black"):
                            elif cor_casa == "black":
                                # Casa zero é a posição de Início
                                player.pos = 0 
                                scene.message = f"{player.name} tirou {scene.last_roll}, caiu na PRETA! Voltou ao inicio."
                                phase = "next"
                                
                            # SENÃO (Para casas "white", "start" e "end" - não fazem nada):
                            else: 
                                scene.message = f"{player.name} tirou {scene.last_roll} e andou em seguranca."
                                phase = "next"

                            # --- REQUISITO 5: FIM DO JOGO ---
                            
                            # Se a vida do jogador atual chegou a zero (ou menos):
                            if player.life <= 0:
                                # Usa divisão com resto (%) para descobrir quem é o "outro" jogador (o vencedor)
                                vencedor = scene.players[(scene.current_idx + 1) % len(scene.players)]
                                # Anuncia a morte e o vencedor
                                scene.message = f"{player.name} morreu! VENCEDOR: {vencedor.name} (Vida {vencedor.life})"
                                # Trava o jogo na fase de "Game Over"
                                phase = "game_over"
                            
                            # SENÃO, SE a posição do jogador for a última casa do tabuleiro:
                            elif player.pos >= perimeter_length - 1: 
                                scene.message = f"FIM DE JOGO! VENCEDOR: {player.name} (Vida {player.life})"
                                # Trava o jogo na fase de "Game Over"
                                phase = "game_over"

                    # Se a fase for "next" (Passar o turno)...
                    elif phase == "next":
                        # Muda o índice do jogador (De 0 para 1, de 1 para 0)
                        scene.current_idx = (scene.current_idx + 1) % len(scene.players)
                        # Devolve o jogo para a fase de rolar os dados
                        phase = "roll"
                        
                        # Verifica se o jogador que acabou de receber o turno está amordaçado (preso na amarela)
                        if hasattr(scene.players[scene.current_idx], 'skip_turn') and scene.players[scene.current_idx].skip_turn:
                             scene.message = f"Vez de {scene.players[scene.current_idx].name} (Preso - Aperte espaco)"
                        # Se não estiver preso, só avisa de quem é a vez normalmente
                        else:
                             scene.message = f"Vez de {scene.players[scene.current_idx].name}"
                    
                    # Se a fase for de fim de jogo, o comando "pass" impede que o botão de espaço faça qualquer coisa
                    elif phase == "game_over":
                        pass
        # Sincroniza a posição atualizada do Código 1 com o renderizador visual
        for jogador in jogadores:
            jogador.posicao = jogador.pos

        # Atualiza o texto do painel dinamicamente usando as informações de 'scene' e 'phase'
        mensagem_principal = f"Vez: {scene.players[scene.current_idx].name} | Fase: {phase}"
        mensagem_secundaria = scene.message if scene.message else "Pressione ESPACO para jogar"

        desenhar_tabuleiro(tela, tabuleiro)
        desenhar_jogadores(tela, jogadores, posicoes_perimetro)
        desenhar_painel(tela, mensagem_principal, mensagem_secundaria, fonte)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()