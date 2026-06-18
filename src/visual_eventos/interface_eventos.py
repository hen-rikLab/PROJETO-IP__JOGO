import pygame  # Importa a biblioteca do Pygame para termos acesso às funções gráficas

# OBRIGATÓRIO: Inicializa o módulo interno de fontes do Pygame para podermos renderizar textos
pygame.font.init()

# Cria o objeto de fonte para o histórico de ações (Arial, tamanho 16, padrão)
FONTE_LOGS = pygame.font.SysFont("Arial", 16)               
# Cria o objeto de fonte para os cards dos jogadores (Arial, tamanho 14, em negrito)
FONTE_STATUS_PLAYER = pygame.font.SysFont("Arial", 14, bold=True) 
# Cria o objeto de fonte para os pop-ups normais (Arial, tamanho 32, em negrito)
FONTE_ALERTA = pygame.font.SysFont("Arial", 32, bold=True)  
# Cria o objeto de fonte para o letreiro gigante do campeão (Arial, tamanho 42, em negrito)
FONTE_VENCEDOR_DESTAQUE = pygame.font.SysFont("Arial", 42, bold=True) 

# Define a cor RGB para o texto comum do histórico (Branco acinzentado)
COR_TEXTO_PADRAO = (240, 240, 240)
# Define a cor RGB para os títulos dos alertas e bordas dos pop-ups (Dourado)
COR_ALERTA_CENTRAL = (255, 215, 0)
# Define a cor RGB para o corpo do dado geométrico (Branco Marfim)
COR_DADO_FUNDO = (245, 245, 245)  
# Define a cor RGB para as bolinhas indicadoras de valor do dado (Grafite Escuro)
COR_DADO_PONTOS = (20, 20, 20)     

# Inicializa a lista que guardará até 4 linhas de histórico no painel inferior
historico_eventos = []
# Cria uma string vazia para rastrear e evitar que a mesma mensagem entre repetida no histórico
ultima_mensagem_rastreada = ""
# Inicializa a string que armazenará o texto ativo a ser exibido no pop-up central
mensagem_alerta = ""
# Inicializa o contador de frames do pop-up (determina por quanto tempo ele fica visível)
tempo_alerta_restante = 0
# Inicializa a variável global que armazena o número atual do dado (de 1 a 6)
valor_dado_atual = 0  

def disparar_alerta_central(texto):
    """Função global para ativar o pop-up no centro da tela e definir sua duração."""
    global mensagem_alerta, tempo_alerta_restante  # Permite modificar as variáveis globais de controle
    mensagem_alerta = texto  # Guarda o texto recebido na variável que o pop-up lê
    tempo_alerta_restante = 120  # Define a duração para 120 frames (equivalente a 2 segundos em 60 FPS)

def desenhar_painel_refinado(tela, msg_principal, msg_secundaria, jogadores):
    """Desenha a barra preta inferior, alimenta o histórico e gerencia os status de vida."""
    global historico_eventos, ultima_mensagem_rastreada, valor_dado_atual  # Puxa as globais necessárias
    
    largura_tela = tela.get_width()  # Captura dinamicamente a largura atual da janela do jogo
    altura_tela = tela.get_height()  # Captura dinamicamente a altura atual da janela do jogo
    altura_painel = 150  # Define a altura fixa da barra escura do painel (150 pixels)
    y_painel = altura_tela - altura_painel  # Calcula a coordenada Y inicial do painel (rodape da tela)
    
    largura_box = 160  # Define a largura de cada uma das caixas de vida dos jogadores
    altura_box = 48  # Define a altura de cada uma das caixas de vida dos jogadores
    x_boxes = largura_tela - largura_box - 20   # Posiciona os cards recuando 20 pixels da borda direita

    # Verifica se há uma nova mensagem secundária e se ela é diferente da última gravada
    if msg_secundaria and msg_secundaria != ultima_mensagem_rastreada:
        # Filtro de segurança: Se a mensagem contiver "Vida final", ela é ignorada para não poluir o painel
        if "Vida final" not in msg_secundaria and "Vida do vencedor" not in msg_secundaria:
            historico_eventos.append(msg_secundaria)  # Adiciona a nova mensagem na lista do histórico
            ultima_mensagem_rastreada = msg_secundaria  # Atualiza o rastreador para evitar repetições
            
            # Se o jogador pisar em uma casa colorida de efeito, ativa o pop-up central imediatamente
            if "VERMELHA" in msg_secundaria or "VERDE" in msg_secundaria or "AMARELA" in msg_secundaria or "PRETA" in msg_secundaria:
                disparar_alerta_central(msg_secundaria)  # Passa o texto do evento para a função de alerta
                
            # Mantém a lista do histórico compacta tirando a linha mais antiga se passar de 4 itens
            if len(historico_eventos) > 4:
                historico_eventos.pop(0)  # Remove o primeiro item da lista (índice 0)

    # Verifica se a mensagem de cima (ciano) anuncia o vencedor do jogo
    if "VENCEDOR" in msg_principal and mensagem_alerta != msg_principal:
        disparar_alerta_central(msg_principal)  # Transforma o anúncio de vitória no pop-up central principal

    # Tenta ler dinamicamente o número do dado contido na string da mensagem principal
    if "Ultimo lance:" in msg_principal:
        try:
            partes_lance = msg_principal.split("Ultimo lance:")  # Divide o texto na palavra chave
            valor_dado_atual = int(partes_lance[1].strip())  # Converte o número limpo de texto para número inteiro
        except:
            pass  # Se algo falhar na conversão, o código ignora e não trava o jogo

    # 1. DESENHO DO FUNDO DO PAINEL
    # Desenha o retângulo cinza escuro (RGB 25,25,25) preenchendo toda a extensão do rodapé
    pygame.draw.rect(tela, (25, 25, 25), (0, y_painel, largura_tela, altura_painel))
    # Desenha a linha fina cinza claro (RGB 70,70,70) no topo do painel separando ele do mapa do jogo
    pygame.draw.line(tela, (70, 70, 70), (0, y_painel), (largura_tela, y_painel), 2)
    
    # 2. SISTEMA DE RECORTE DE TEXTO (ÁREA SEGURA)
    limite_largura_texto = x_boxes - 30   # Calcula o espaço máximo que o texto pode correr antes de encostar nos cards
    # Cria uma superfície invisível dedicada para as letras com canal Alpha (transparência habilitada)
    superficie_texto_painel = pygame.Surface((limite_largura_texto, altura_painel), pygame.SRCALPHA)

    # Renderiza o texto principal da vez do jogador em cor ciano (RGB 0,255,255)
    superficie_principal = FONTE_LOGS.render(msg_principal, True, (0, 255, 255))
    # Carimba o texto principal na posição interna da sub-superfície
    superficie_texto_painel.blit(superficie_principal, (20, 15))
    
    y_texto = 45  # Define a altura inicial onde a primeira linha do histórico vai começar a ser impressa
    # Percorre a lista de histórico desenhando linha por linha de forma empilhada
    for idx, evento in enumerate(historico_eventos):
        # Renderiza o texto da ação com um ponto marcador estilizado na cor padrão
        superficie_evento = FONTE_LOGS.render(f"• {evento}", True, COR_TEXTO_PADRAO)
        # Carimba o texto aplicando 22 pixels de espaçamento vertical multiplicado pelo índice da linha
        superficie_texto_painel.blit(superficie_evento, (20, y_texto + (idx * 22)))
        
    # Transfere a sub-superfície de textos completa para a tela real do jogo, aplicando o recorte automático
    tela.blit(superficie_texto_painel, (0, y_painel))

    # 3. DESENHO DOS CARDS DE VIDA E STATUS (CANTO DIREITO)
    cores_jogadores = [(255, 193, 7), (155, 89, 182)]   # Lista de cores das bordas (Amarelo para Player 1, Roxo para Player 2)

    # Percorre a lista de objetos de jogadores que veio do loop principal da main.py
    for idx, jg in enumerate(jogadores):
        # Calcula o posicionamento Y de cada card somando um recuo inicial e o espaçamento proporcional entre eles
        y_box = (y_painel + 22) + (idx * (altura_box + 10))
        
        # Desenha a caixa cinza de fundo (RGB 40,40,40) de cada card com bordas arredondadas em 6 pixels
        pygame.draw.rect(tela, (40, 40, 40), (x_boxes, y_box, largura_box, altura_box), border_radius=6)
        # Escolhe a cor da borda baseado no índice do jogador ou usa cinza se houver mais players
        cor_player = cores_jogadores[idx] if idx < len(cores_jogadores) else (100, 100, 100)
        # Aplica o contorno fino colorido no card usando a cor definida e raio de canto de 6 pixels
        pygame.draw.rect(tela, cor_player, (x_boxes, y_box, largura_box, altura_box), width=1, border_radius=6)
        
        txt_nome = f"{jg.nome}"  # Captura a string de nome direto do atributo .nome do objeto do jogador
        txt_vida = f"Vida: {jg.life}"  # Captura o valor da vida direto do atributo .life do objeto do jogador
        
        # Renderiza o nome do jogador na cor cinza claro padrão
        surf_nome = FONTE_STATUS_PLAYER.render(txt_nome, True, COR_TEXTO_PADRAO)
        # Define dinamicamente a cor da vida: Fica Vermelho se tiver 3 ou menos de vida, senão fica Verde
        cor_texto_vida = (255, 100, 100) if jg.life <= 3 else (100, 255, 100)
        # Renderiza o texto numérico da vida com a cor dinâmica escolhida acima
        surf_vida = FONTE_STATUS_PLAYER.render(txt_vida, True, cor_texto_vida)
        
        # Desenha o nome dentro do card respeitando o recuo interno (padding)
        tela.blit(surf_nome, (x_boxes + 12, y_box + 6))
        # Desenha a vida logo abaixo do nome dentro da caixinha correspondente
        tela.blit(surf_vida, (x_boxes + 12, y_box + 24))


def desenhar_dado_central(tela, valor):
    """Renderiza geometricamente um dado D6 clássico de tabuleiro usando vetores nativos."""
    if valor < 1 or valor > 6:
        return  # Bloqueio de segurança: Se não houver jogada ou o valor for inválido, sai da função sem desenhar

    largura_tela = tela.get_width()  # Pega a largura do display do jogo
    altura_tela = tela.get_height()  # Pega a altura do display do jogo
    
    tamanho_dado = 70  # Define a dimensão quadrada do bloco do dado (70x70 pixels)
    x_dado = (largura_tela // 2) - (tamanho_dado // 2)  # Centraliza o dado na horizontal
    y_dado = (altura_tela // 2) - (tamanho_dado // 2) - 60   # Posiciona o dado na vertical deslocado 60px para cima do meio
    
    # Desenha um retângulo escuro translúcido deslocado 4 pixels para baixo e para o lado criando efeito de sombra projetada
    pygame.draw.rect(tela, (10, 10, 10, 100), (x_dado + 4, y_dado + 4, tamanho_dado, tamanho_dado), border_radius=10) 
    # Desenha o corpo principal quadrado do dado na cor branca marfim com cantos arredondados
    pygame.draw.rect(tela, COR_DADO_FUNDO, (x_dado, y_dado, tamanho_dado, tamanho_dado), border_radius=10)
    # Desenha um contorno sutil cinza nas bordas do quadrado branco para dar efeito de profundidade 2D
    pygame.draw.rect(tela, (180, 180, 180), (x_dado, y_dado, tamanho_dado, tamanho_dado), width=2, border_radius=10) 
    
    # MATEMÁTICA DAS COORDENADAS: Mapeia as posições físicas dos pontos (bolinhas) dentro do quadrado do dado
    p_centro = (x_dado + tamanho_dado // 2, y_dado + tamanho_dado // 2)  # Ponto central exato
    p_top_esq = (x_dado + 18, y_dado + 18)  # Ponto superior esquerdo
    p_top_dir = (x_dado + tamanho_dado - 18, y_dado + 18)  # Ponto superior direito
    p_mid_esq = (x_dado + 18, y_dado + tamanho_dado // 2)  # Ponto médio esquerdo
    p_mid_dir = (x_dado + tamanho_dado - 18, y_dado + tamanho_dado // 2)  # Ponto médio direito
    p_bot_esq = (x_dado + 18, y_dado + tamanho_dado - 18)  # Ponto inferior esquerdo
    p_bot_dir = (x_dado + tamanho_dado - 18, y_dado + tamanho_dado - 18)  # Ponto inferior direito
    
    raio_ponto = 6  # Define o raio físico em pixels de cada bolinha do dado
    
    # ESTRUTURA LÓGICA DO DADO: Associa quais pontos geométricos devem ser acesos para cada valor numérico tirado
    pontos_para_desenhar = []
    if valor == 1:
        pontos_para_desenhar = [p_centro]
    elif valor == 2:
        pontos_para_desenhar = [p_top_esq, p_bot_dir]
    elif valor == 3:
        pontos_para_desenhar = [p_top_esq, p_centro, p_bot_dir]
    elif valor == 4:
        pontos_para_desenhar = [p_top_esq, p_top_dir, p_bot_esq, p_bot_dir]
    elif valor == 5:
        pontos_para_desenhar = [p_top_esq, p_top_dir, p_centro, p_bot_esq, p_bot_dir]
    elif valor == 6:
        pontos_para_desenhar = [p_top_esq, p_top_dir, p_mid_esq, p_mid_dir, p_bot_esq, p_bot_dir]

    # Laço que percorre os pontos selecionados no bloco lógico acima e os pinta fisicamente na tela
    for pt in pontos_para_desenhar:
        pygame.draw.circle(tela, COR_DADO_PONTOS, pt, raio_ponto)  # Desenha os círculos preenchidos de grafite escuro


def desenhar_alerta_central(tela):
    """Controla o gerenciamento de pop-ups na tela. Se não houver pop-up ativo, exibe o dado geométrico."""
    global mensagem_alerta, tempo_alerta_restante, valor_dado_atual  # Carrega o controle global
    
    # Se o temporizador de alertas for maior que zero, significa que um pop-up deve estar ativo na tela
    if tempo_alerta_restante > 0:
        largura_tela = tela.get_width()  # Pega a largura do display
        altura_tela = tela.get_height()  # Pega a altura do display
        
        # CASO ESPECIAL: Se for uma string contendo o anúncio de fim de jogo com vencedor
        if "VENCEDOR:" in mensagem_alerta:
            partes = mensagem_alerta.split("VENCEDOR:")  # Separa o texto dividindo pelos dois pontos
            nome_jogador = partes[1].strip() if len(partes) > 1 else "Jogador"  # Isola apenas o nome limpo do campeão
            
            # Renderiza a linha de cima em formato menor usando cor padrão esbranquiçada
            surf_linha1 = FONTE_ALERTA.render("O vencedor foi...", True, COR_TEXTO_PADRAO)
            # Renderiza o nome do campeão na linha de baixo usando a fonte gigante em dourado
            surf_linha2 = FONTE_VENCEDOR_DESTAQUE.render(nome_jogador, True, COR_ALERTA_CENTRAL)
            
            # Ajusta dinamicamente a largura da caixa preta baseado em qual das duas linhas de texto ficou mais larga
            largura_box = max(surf_linha1.get_width(), surf_linha2.get_width()) + 60
            # Soma a altura das duas fontes mais um espaçamento interno de margem (padding)
            altura_box = surf_linha1.get_height() + surf_linha2.get_height() + 40
            
            # Define o posicionamento horizontal e eleva o pop-up aplicando a correção de -60 pixels para cima
            x_box = (largura_tela // 2) - (largura_box // 2)
            y_box = (altura_tela // 2) - (altura_box // 2) - 60
            
            # Cria a superfície translúcida de fundo para o container de vitória
            box_surface = pygame.Surface((largura_box, altura_box), pygame.SRCALPHA)
            # Desenha o retângulo preto de fundo com opacidade alta (230) e cantos arredondados em 12 pixels
            pygame.draw.rect(box_surface, (0, 0, 0, 230), (0, 0, largura_box, altura_box), border_radius=12)
            # Desenha a moldura fina externa dourada ao redor do bloco com cantos arredondados de 12 pixels
            pygame.draw.rect(box_surface, COR_ALERTA_CENTRAL, (0, 0, largura_box, altura_box), width=2, border_radius=12)
            tela.blit(box_surface, (x_box, y_box))  # Projeta o contêiner de fundo na janela principal
            
            # Centraliza a primeira linha ("O vencedor foi...") horizontalmente dentro do espaço da caixinha
            x_l1 = x_box + (largura_box // 2) - (surf_linha1.get_width() // 2)
            y_l1 = y_box + 15  # Aplica um recuo de 15 pixels do topo da caixa
            tela.blit(surf_linha1, (x_l1, y_l1))  # Desenha o texto na tela
            
            # Centraliza o nome do jogador em destaque logo abaixo da primeira linha
            x_l2 = x_box + (largura_box // 2) - (surf_linha2.get_width() // 2)
            y_l2 = y_l1 + surf_linha1.get_height() + 10  # Posiciona 10 pixels abaixo do fim da primeira linha
            tela.blit(surf_linha2, (x_l2, y_l2))  # Desenha o nome do campeão em destaque na tela
            
        else:
            # FLUXO PADRÃO: Alertas comuns do tabuleiro (Casas Verde, Vermelha, Amarela...)
            superficie_texto = FONTE_ALERTA.render(mensagem_alerta, True, COR_ALERTA_CENTRAL)
            
            # Ajusta o tamanho da caixinha proporcionalmente ao tamanho da string renderizada
            largura_box = superficie_texto.get_width() + 40
            altura_box = superficie_texto.get_height() + 20
            
            # Calcula a posição centralizada e aplica o mesmo recuo vertical de -60 pixels para cima
            x_box = (largura_tela // 2) - (largura_box // 2)
            y_box = (altura_tela // 2) - (altura_box // 2) - 60
            
            # Monta a superfície com canal de transparência para o alerta padrão
            box_surface = pygame.Surface((largura_box, altura_box), pygame.SRCALPHA)
            # Desenha o fundo preto com opacidade levemente mais suave (220) e cantos arredondados em 10 pixels
            pygame.draw.rect(box_surface, (0, 0, 0, 220), (0, 0, largura_box, altura_box), border_radius=10)
            # Desenha o contorno dourado ao redor do pop-up padrão
            pygame.draw.rect(box_surface, COR_ALERTA_CENTRAL, (0, 0, largura_box, altura_box), width=2, border_radius=10)
            
            tela.blit(box_surface, (x_box, y_box))  # Desenha o container na tela
            tela.blit(superficie_texto, (x_box + 20, y_box + 10))  # Centraliza o texto interno dentro da caixa
        
        tempo_alerta_restante -= 1  # Subtrai 1 frame da vida útil do pop-up a cada iteração do loop do jogo
    else:
        # SE NÃO HOUVER ALERTA ATIVO NA TELA: O jogo fica livre para renderizar o dado geométrico no centro
        desenhar_dado_central(tela, valor_dado_atual)  # Passa o valor atual salvo para a função gráfica do dado