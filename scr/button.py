import pygame

class Button:

    def __init__(self, id, x, y, w, h, image, screen, text, font, color):
        self.id = id
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = image
        self.image = pygame.transform.scale(self.image, (w, h))
        self.screen = screen
        self.text = text
        self.font = font
        self.color = color

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
        """pygame.draw.rect(self.screen, "blue", pygame.Rect(self.x, self.y, self.w, self.h))
        pygame.draw.rect(self.screen, "white", pygame.Rect(self.x+2, self.y+2, self.w-4, self.h-4))"""
        self.buttonText = self.font.render(self.text, True, self.color)
        self.screen.blit(self.buttonText, (self.x + self.w // 2 - self.buttonText.get_rect()[2]//2, self.y + self.h // 2 - self.buttonText.get_rect()[3]//2))

    def collide(self, x, y):
        if self.x <= x and self.x + self.w >= x:
            if self.y <= y and self.y + self.h >= y:
                return True
        return False