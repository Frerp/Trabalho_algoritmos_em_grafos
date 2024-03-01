import pygame
import sys
from gui.buttons import Button  # Import adicionado para a classe Button
import random
clock = pygame.time.Clock()

class Character:
    def __init__(self, image_path, initial_vertex, health, attack):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = initial_vertex
        self.current_vertex = initial_vertex
        self.health = health
        self.attack = attack
        self.enemies = []

    def move_to_vertex(self, target_vertex):
        self.rect.center = target_vertex
        self.current_vertex = target_vertex

    def move_to_random_adjacent_vertex(self, lista_adjacencias, vertices_pos):
        current_vertex_id = vertices_pos.index(self.current_vertex) + 1
        adjacentes = lista_adjacencias[current_vertex_id]
        target_vertex = random.choice(adjacentes)
        self.current_vertex = vertices_pos[target_vertex - 1]
        self.move_to_vertex(self.current_vertex)

    def take_damage(self, damage):
        self.health -= damage

    def attack_enemy(self, enemy):
        enemy.take_damage(self.attack)

    def handle_enemy_event(self, enemy, screen):  # Adicionado parâmetro screen
        print(f"Você encontrou um {enemy.name}!")
        print(f"Pontos de Vida do {enemy.name}: {enemy.health}")
        print("Escolha o que fazer:")
        print("1. Lutar")
        print("2. Fugir")

        # Utilizando botões para escolha
        buttons = [Button("Lutar", (920, 200), (300, 50)),
                   Button("Fugir", (920, 260), (300, 50))]

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
                if choice == "Lutar":
                    self.attack_enemy(enemy)
                    print(f"Você atacou o {enemy.name}!")
                elif choice == "Fugir":
                    print("Você fugiu do combate.")
                return  # Importante sair do loop quando a escolha é feita

    def handle_healing_event(self, screen):  # Adicionado parâmetro screen
        print("Você encontrou uma cura!")
        print("Escolha o que fazer:")
        print("1. Usar a cura")
        print("2. Ignorar")

        # Utilizando botões para escolha
        buttons = [Button("Usar a cura", (920, 200), (300, 50)),
                   Button("Ignorar", (920, 260), (300, 50))]

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
                    self.health += 20  # Adicione a quantidade desejada de pontos de vida
                    print("Você usou a cura e recuperou pontos de vida!")
                elif choice == "Ignorar":
                    print("Você ignorou a cura.")
                return  # Importante sair do loop quando a escolha é feita

    def handle_weapon_event(self, screen):  # Adicionado parâmetro screen
        print("Você encontrou uma arma!")
        print("Escolha o que fazer:")
        print("1. Pegar a arma e trocar pela atual")
        print("2. Deixar a arma")

        # Utilizando botões para escolha
        buttons = [Button("Pegar a arma", (920, 200), (300, 50)),
                   Button("Deixar a arma", (920, 260), (300, 50))]

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
                    print("Você pegou a nova arma.")
                    # Lógica para trocar a arma atual pela nova
                elif choice == "Deixar a arma":
                    print("Você deixou a arma para trás.")
                return  # Importante sair do loop quando a escolha é feita

    def handle_event(self, event_type, screen):  # Adicionado parâmetro screen
        if event_type == 'inimigo':
            enemy = random.choice(self.enemies)
            self.handle_enemy_event(enemy, screen)
        elif event_type == 'cura':
            self.handle_healing_event(screen)
        elif event_type == 'arma':
            self.handle_weapon_event(screen)

    def render_buttons(self, screen, buttons):
        for button in buttons:
            button.draw(screen)

    def check_button_click(self, buttons, mouse_pos, mouse_click):
        for button in buttons:
            button.update(mouse_pos, mouse_click)
            if button.clicked:
                return button.label
        return None

class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def take_damage(self, damage):
        self.health -= damage

    def attack_player(self, player):
        player.take_damage(self.attack)
