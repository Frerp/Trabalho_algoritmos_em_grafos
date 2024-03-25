import pygame
import sys
from gui.buttons import Button
import random
from characters.enemy import Enemy
from characters.heal import Heal
from characters.weapon import Weapon
from characters.treasure import Treasure

clock = pygame.time.Clock()

class Character:
    def __init__(self, initial_vertex, index_initial_vertex, health, attack):
        self.sprites = []
        self.sprites.append(pygame.image.load('Animacao_Personagem/Personagem_Animação_1.png'))
        self.sprites.append(pygame.image.load('Animacao_Personagem/Personagem_Animação_2.png'))
        self.sprites.append(pygame.image.load('Animacao_Personagem/Personagem_Animação_3.png'))
        self.sprites.append(pygame.image.load('Animacao_Personagem/Personagem_Animação_4.png'))
        self.sprites.append(pygame.image.load('Animacao_Personagem/Personagem_Animação_5.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect()
        self.rect.center = (initial_vertex[0] + 30, initial_vertex[1] - 30)
        self.current_vertex = initial_vertex
        self.index_current_vertex = index_initial_vertex
        self.health = health
        self.attack = attack
        self.bullets = 0
        self.time = 0
        
    def update_sprite(self):
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.image = pygame.transform.scale(self.image, (120, 120))

    def move_to_vertex(self, target_vertex, index_target_vertex):
        self.rect.center = (target_vertex[0] + 30, target_vertex[1] - 30)
        self.previous_vertex = self.current_vertex
        self.current_vertex = target_vertex

        self.index_current_vertex = index_target_vertex

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

    def attack_enemy(self, enemy):
        enemy.take_damage(self.attack)


    def handle_enemy_event(self, enemy, screen):
        print(f"Você encontrou um {enemy.name}!")
        print(f"Pontos de Vida do {enemy.name}: {enemy.health}")

        # Criar nova tela para o combate
        combat_screen = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("Combate")

        #carregar imagem background
        if 0 <= self.time <= 35:
            background_image = pygame.image.load("Assets/background_manha.jpeg")
        elif 36 <= self.time <= 70:
            background_image = pygame.image.load("Assets/background tarde.jpeg")
        elif 71 <= self.time:   
            background_image = pygame.image.load("Assets/background noite.jpeg")

        # Carregar imagens do jogador e do inimigo
        player_image = pygame.image.load("Assets/Anderson.png")
        enemy_image = pygame.image.load(enemy.image_path)

        # Redimensionar imagens
        player_image = pygame.transform.scale(player_image, (150, 150))
        enemy_image = pygame.transform.scale(enemy_image, (150, 150))
        background_image = pygame.transform.scale(background_image, (1200, 600))

        # Definir posição inicial das imagens
        player_rect = player_image.get_rect(center=(200, 300))
        enemy_rect = enemy_image.get_rect(center=(600, 300))
        background_rect = background_image.get_rect(center=(600, 300))

        # Exibir imagens na tela de combate
        combat_screen.blit(background_image, background_rect)
        combat_screen.blit(player_image, player_rect)
        combat_screen.blit(enemy_image, enemy_rect)
        pygame.display.flip()

        # Animação da aproximação do jogador em direção ao inimigo
        start_position = player_rect.center
        end_position = (enemy_rect.center[0] - 130, enemy_rect.center[1])  # Move o jogador um pouco para a esquerda
        move_vector = (end_position[0] - start_position[0], end_position[1] - start_position[1])
        for i in range(25):
            move_offset = (move_vector[0] * i / 25, move_vector[1] * i / 25)
            player_position = (start_position[0] + move_offset[0], start_position[1] + move_offset[1])
            combat_screen.fill((0, 0, 0))  # Limpar tela
            combat_screen.blit(background_image, background_rect)
            combat_screen.blit(player_image, player_position)
            combat_screen.blit(enemy_image, enemy_rect.center)
            pygame.display.flip()
            clock.tick(60)

        # Exibir botões de ação
        buttons = [Button("Lutar", (390, 470), (200, 80), 'Assets/Combat_Button.png'), Button("Fugir", (620, 470), (200, 80), 'Assets/Run_button.png')]
        for button in buttons:
            button.draw(combat_screen)
        pygame.display.flip()

        # Continuar a interação de combate normalmente
        while self.health > 0 and enemy.health > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            choice = self.check_button_click(buttons, mouse_pos, mouse_click)
            if choice:
                if choice == "Lutar":

                    player_damage = random.randint(1, self.attack)
                    print(f"Você atacou o {enemy.name} e causou {player_damage} de dano!")
                    enemy.health -= player_damage
                    if self.attack > 21 :
                        self.bullets -= 1
                        if self.bullets <= 0:
                            self.attack = 20
                    if enemy.health <= 0:
                        print(f"Você derrotou o {enemy.name}!")
                        return "inimigo morreu"

                    enemy_damage = random.randint(1, enemy.attack)
                    print(f"{enemy.name} atacou você e causou {enemy_damage} de dano!")
                    self.take_damage(enemy_damage)


                    if self.health <= 0:
                        print("Você foi derrotado!")
                        return "jogador morreu"

                    
                    pygame.display.flip()

                elif choice == "Fugir":
                    enemy_damage = random.randint(1, enemy.attack)
                    self.health -= enemy_damage
                    print("Você escolheu fugir!")
                    return


    def handle_healing_event(self, heal,screen):
        print("Você encontrou uma cura!")
        print("Escolha o que fazer:")
        print("1. Usar a cura")
        print("2. Ignorar")

        buttons = [Button("Usar a cura", (840, 475), (160, 70), 'Assets/Take_heal_button.png'),
                   Button("Ignorar", (1005, 475), (160, 70), 'Assets/Leave_heal_button.png')]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.render_buttons(screen, buttons)
            pygame.display.flip()
            clock.tick(30)

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            choice = self.check_button_click(buttons, mouse_pos, mouse_click)
            if choice:
                if choice == "Usar a cura":
                    self.health += heal.healing_points
                    if self.health >= 100 :
                        self.health = 100
                    print("Você usou a cura e recuperou pontos de vida!")
                    return "cura usada"
                elif choice == "Ignorar":
                    print("Você ignorou a cura.")
                return

    def handle_weapon_event(self, weapon, screen):
        print("Você encontrou uma arma!")
        print("Escolha o que fazer:")
        print("1. Pegar a arma e trocar pela atual")
        print("2. Deixar a arma")

        buttons = [Button("Pegar a arma", (840, 475), (160, 70), 'Assets/Take_weapon_button.png'),
                   Button("Deixar a arma",  (1005, 475), (160, 70), 'Assets/Leave_weapon_button.png')]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.render_buttons(screen, buttons)
            pygame.display.flip()
            clock.tick(30)

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            choice = self.check_button_click(buttons, mouse_pos, mouse_click)
            if choice:
                if choice == "Pegar a arma":
                    self.attack = 20 + weapon.damage
                    self.bullets = weapon.bullets
                    print("Você pegou a nova arma.")
                    return "arma usada"
                elif choice == "Deixar a arma":
                    print("Você deixou a arma para trás.")
                return

    def handle_map_event(self, map, screen):
        print("Você encontrou um mapa!")
        print("Escolha o que fazer:")
        print("1. Pegar o mapa!")
        print("2. Deixar o mapa.")

        buttons = [Button("Pegar o mapa", (840, 475), (160, 70), 'Assets/Take_map_button.png'),
                   Button("Deixar o mapa",  (1005, 475), (160, 70), 'Assets/Leave_map_button.png')]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.render_buttons(screen, buttons)
            pygame.display.flip()
            clock.tick(30)

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            choice = self.check_button_click(buttons, mouse_pos, mouse_click)
            if choice:
                if choice == "Pegar o mapa":
                    print("Você pegou o mapa")
                    return 'Peguei o mapa'
                elif choice == "Deixar o mapa":
                    print("Você deixou o mapa para trás.")
                    return 'Deixei o mapa'

    def handle_checkpoint_event(self, checkpoint, screen):
        print("Você chegou a um checkpoint!")

        buttons = [Button("OK!", (900, 475), (200, 75), 'Assets/Checkpoint_button.png')]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.render_buttons(screen, buttons)
            pygame.display.flip()
            clock.tick(30)

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            choice = self.check_button_click(buttons, mouse_pos, mouse_click)
            if choice:
                return        

    def handle_treasure_event(self, event_object, screen):
        treasure_object = Treasure('tesouro', 100)
        return treasure_object

    def handle_event(self, event_object, screen):
        if event_object.type == 'inimigo':
            resultado = self.handle_enemy_event(event_object, screen)
            return resultado
        elif event_object.type == 'cura':
            resultado =  self.handle_healing_event(event_object, screen)
            return resultado
        elif event_object.type == 'arma':
            resultado =  self.handle_weapon_event(event_object, screen)
            return resultado
        elif event_object.type == 'terreno':
            self.handle_weapon_event(event_object, screen)
        elif event_object.type == 'mapa':
            resultado = self.handle_map_event(event_object, screen)
            return resultado
        elif event_object.type == 'checkpoint':
            self.handle_checkpoint_event(event_object, screen)
        elif event_object.type == 'tesouro':
            resposta = self.handle_treasure_event(event_object, screen)
            return resposta

    def render_buttons(self, screen, buttons):
        for button in buttons:
            button.draw(screen)

    def check_button_click(self, buttons, mouse_pos, mouse_click):
        for button in buttons:
            button.update(mouse_pos, mouse_click)
            if button.clicked:
                return button.label
        return None
