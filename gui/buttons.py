# buttons.py
import pygame

class Button:
    def __init__(self, label, position, size):
        self.label = label
        self.position = position
        self.size = size
        self.rect = pygame.Rect(self.position, self.size)
        self.clicked = False
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        text = self.font.render(self.label, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def update(self, mouse_pos, mouse_click):
        if self.rect.collidepoint(mouse_pos):
            if mouse_click[0] == 1:  # 1 significa clique do botão esquerdo do mouse
                self.clicked = True
            else:
                self.clicked = False
        else:
            self.clicked = False
