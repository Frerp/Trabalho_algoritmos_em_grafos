# buttons.py
import pygame

class Button:
    def __init__(self, label, position, size, image_path):
        self.label = label
        self.position = position
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.size = size
        self.rect = pygame.Rect(self.position, self.size)
        self.clicked = False
        #self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        screen.blit(self.image, self.position)


    def update(self, mouse_pos, mouse_click):
        if self.rect.collidepoint(mouse_pos):
            if mouse_click[0] == 1:  # 1 significa clique do botão esquerdo do mouse
                self.clicked = True
            else:
                self.clicked = False
        else:
            self.clicked = False
