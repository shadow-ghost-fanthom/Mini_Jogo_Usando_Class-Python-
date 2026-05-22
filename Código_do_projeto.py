import time, keyboard, random, os, string

# ==========================================
# CLASSE DO JOGADOR
# ==========================================
class Jogador():
    def __init__(self, Nick, HP, ATK):
        self.Nick = Nick  # Nome do jogador
        self.HP = HP      # Pontos de vida atuais
        self.ATK = ATK    # Texto descritivo do dano da classe
    
    def atacar(self, alvo):
        # Loop de espera até que o jogador pressione a tecla de ataque
        while True:
            if keyboard.is_pressed('f'):
                # Define o dano aleatório com base na classe escolhida
                match classe:
                    case 1:
                        dano = random.randint(5, 20)      # Mago
                    case 2:
                        dano = random.randint(3, 10)      # Guerreiro
                    case 3:
                        dano = random.randint(10, 40)     # Assassino

                # Aplica o dano diretamente no HP do monstro (alvo)
                alvo.HP -= dano
                print(f"O Player atacou! Tirou {dano} de dano.")
                return # Sai do loop e encerra o turno do jogador
                    
            time.sleep(0.1) # Evita sobrecarregar o processador no loop

# ==========================================
# CLASSE DO MONSTRO
# ==========================================
class Monstro:
    def __init__(self, Nick, HP):
        self.Nick = Nick  # Nome do monstro
        self.HP = HP      # Pontos de vida do monstro

    def atacar(self, alvo):
        x = 3 # Tempo inicial do countdown de preparação

        # Anúncio do ataque do monstro
        print("-=" * 15)
        print(f"{'O monstro vai atacar! Preparesse'}")
        print("-=" * 15)
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')

        # Loop da contagem regressiva visual (3, 2, 1)
        for i in range(1, 4):
            print("-=" * 15)
            print(f"{x:^30}")
            print("-=" * 15)
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            x -= 1
        
        # Ajusta a janela de tempo de reação baseado na classe do jogador (Nerf/Buff)
        if classe == 3:
            x = 2      # Assassino ganha mais tempo por ter apenas 1 de HP
        else:
            x = 1.5    # Outras classes têm menos tempo

        # Sorteia uma letra aleatória do alfabeto para o Quick Time Event (QTE)
        letra = random.choice(string.ascii_lowercase)
        
        # Loop do cronômetro de esquiva (QTE)
        while x >= 0:
            print("-=" * 21)
            print(f"{f'APERTE \033[1;33m{letra.upper()}\033[0m':^50}") # Letra colorida em amarelo
            print("-=" * 21)
            print(f">> {x:.1f}", flush=True)
            x -= 0.1

            # Se o jogador apertar a letra certa a tempo, ele esquiva e não toma dano
            if keyboard.is_pressed(letra):
                print("Que desvio!")
                return # Encerra o turno do monstro sem causar dano

            time.sleep(0.1)
            os.system('cls' if os.name == 'nt' else 'clear')

        # Caso o tempo acabe e o jogador não desvie, calcula o dano do monstro
        dano_monstro = random.randint(20, 50)
        alvo.HP -= dano_monstro # Deduz a vida do jogador (alvo)
        
        # Feedback do ataque do monstro (Normal vs Crítico)
        match dano_monstro:
            case _ if dano_monstro < 33:
                print(f"O montro atacou! Tirou {dano_monstro} de HP")
                return
            
            case _ if dano_monstro > 33:
                print(f"O montro atacou e deu um critico! Tirou {dano_monstro} de HP")
                return

# ==========================================
# CRIAÇÃO DO PERSONAGEM (INPUTS DO USUÁRIO)
# ==========================================
print("-=" * 15)            
print(f"{'Qual seu nome jogador?':^30}")
print("-=" * 15)            
nome = input(">> ")
os.system('cls' if os.name == 'nt' else 'clear')

print("-=" * 18)
print(f"{'ESCOLHA SUA CLASSE!':^35}")
print(f"{'Mago = 1':^35}")
print(f"{'Guerreiro = 2':^35}")
print(f"{'Assassino = 3':^35}")
print("-=" * 18)
try:
    classe = int(input(">> "))
except ValueError:
    print("Você não digitou um valor válido")
os.system('cls' if os.name == 'nt' else 'clear')

# Instancia o objeto do jogador com atributos específicos da classe escolhida
match classe:
    case 1:
        mago = Jogador(nome, 100, "5 a 20")
        player = mago
    case 2:    
        guerreiro = Jogador(nome, 200, "3 a 10")
        player = guerreiro
    case 3:    
        assassino = Jogador(nome, 1, "10 a 40")
        player = assassino
    case _:
        print("Você não escolheu nenhuma classe...")
        exit()

# Exibe os atributos iniciais confirmados
print(f"Status da sua classe: HP = {player.HP} | ATK = {player.ATK}")

# Instancia os possíveis inimigos do jogo
o_guardiao = Monstro("O Guardião!", 200)
slime_gigante = Monstro("Slime Gigante!", 150)
bruxa_sombria = Monstro("Bruxa Sombria!", 100)

# Sorteia qual dos monstros o jogador vai enfrentar nesta partida
monstro_escolhido = random.choice([o_guardiao, slime_gigante, bruxa_sombria])

print(f"Um monstro perigoso apareceu! [{monstro_escolhido.Nick}]")
time.sleep(2)
os.system('cls' if os.name == 'nt' else 'clear')

# ==========================================
# LOOP PRINCIPAL DA BATALHA (GAME LOOP)
# ==========================================
while player.HP > 0 and monstro_escolhido.HP > 0:
    print(f"\nSua Vida: {player.HP} | Vida do Monstro: {monstro_escolhido.HP}")
    print("Sua vez! Pressione 'F' para atacar...")

    # Executa o turno do jogador
    player.atacar(monstro_escolhido)

    # Verifica se o monstro morreu para impedir o contra-ataque dele
    if monstro_escolhido.HP <= 0:
        break

    # Executa o turno do monstro (QTE de esquiva)
    monstro_escolhido.atacar(player)

# ==========================================
# FIM DE JOGO / RESULTADO
# ==========================================
if player.HP > 0:
    print("🎉 VITÓRIA! Você derrotou o monstro!")
else:
    print("💀 GAME OVER! Você foi derrotado...")

input() # Segura a tela final antes de fechar
os.system('cls' if os.name == 'nt' else 'clear')
