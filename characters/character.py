import pygame
import sys
from gui.buttons import Button
import random
from characters.enemy import Enemy

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
        #self.enemies = []

    def move_to_vertex(self, target_vertex):
        self.rect.center = target_vertex
        self.previous_vertex = self.current_vertex
        self.current_vertex = target_vertex

    def take_damage(self, damage):
        self.health -= damage

    def attack_enemy(self, enemy):
        enemy.take_damage(self.attack)

    def handle_enemy_event(self, enemy, screen):
        print(f"Você encontrou um {enemy.name}!")
        print(f"Pontos de Vida do {enemy.name}: {enemy.health}")

        # Exibir imagem do inimigo
        enemy_image = pygame.image.load(enemy.image_path)
        enemy_image = pygame.transform.scale(enemy_image, (150, 150))
        screen.blit(enemy_image, (920, 40))

        print("Escolha o que fazer:")
        print("1. Lutar")
        print("2. Fugir")

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
                    while self.health > 0 and enemy.health > 0:
                        # Ataque do jogador
                        damage_taken = random.randint(1, self.attack)
                        print(f"Você atacou o {enemy.name} e causou {damage_taken} de dano!")
                        enemy.health -= damage_taken

                        if enemy.health <= 0:
                            print(f"Você derrotou o {enemy.name}!")
                            return "inimigo morreu"

                        # Ataque da criatura
                        damage_dealt = random.randint(1, enemy.attack)
                        print(f"{enemy.name} atacou você e causou {damage_dealt} de dano!")
                        self.take_damage(damage_dealt)

                    return
                elif choice == "Fugir":
                    print("Você fugiu do combate.")
                    return
                
    def handle_healing_event(self, heal,screen):
        print("Você encontrou uma cura!")
        print("Escolha o que fazer:")
        print("1. Usar a cura")
        print("2. Ignorar")

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
                    self.health += 20
                    print("Você usou a cura e recuperou pontos de vida!")
                elif choice == "Ignorar":
                    print("Você ignorou a cura.")
                return

    def handle_weapon_event(self, weapon, screen):
        print("Você encontrou uma arma!")
        print("Escolha o que fazer:")
        print("1. Pegar a arma e trocar pela atual")
        print("2. Deixar a arma")

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
                elif choice == "Deixar a arma":
                    print("Você deixou a arma para trás.")
                return

    def handle_checkpoint_event(self, checkpoint, screen):
        print("Você chegou a um checkpoint!")

        buttons = [Button("OK!", (920, 200), (300, 50))]

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

    def handle_event(self, event_object, screen):
        if event_object.type == 'inimigo':
            resultado = self.handle_enemy_event(event_object, screen)
            return resultado
        elif event_object.type == 'cura':
            self.handle_healing_event(event_object, screen)
        elif event_object.type == 'arma':
            self.handle_weapon_event(event_object, screen)
        elif event_object.type == 'terreno':
            pass
            #self.handle
        elif event_object.type == 'checkpoint':
            self.handle_checkpoint_event(event_object, screen)

    def render_buttons(self, screen, buttons):
        for button in buttons:
            button.draw(screen)

    def check_button_click(self, buttons, mouse_pos, mouse_click):
        for button in buttons:
            button.update(mouse_pos, mouse_click)
            if button.clicked:
                return button.label
        return None
