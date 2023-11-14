import pygame

from init import WIDTH, OFFSET

class Coin:

    def __init__(self, x, y = -200):
        self.x = x
        self.y = y

        self.rectCenter = (self.x * WIDTH // 3 + WIDTH // 6, self.y)

    def update(self, screen, speed):
        self.draw(screen)
        self.fall(speed)

    def draw(self, screen):
        self.rectCenter = (self.x * WIDTH // 3 + WIDTH // 6, self.y)
        pygame.draw.circle(screen, "yellow", self.rectCenter, WIDTH // 6 - OFFSET // 2)

    def fall(self, speed):
        self.y += speed

    def getRect(self):
        return pygame.Rect((self.rectCenter[0]- OFFSET // 2, self.rectCenter[1]- OFFSET // 2), (WIDTH // 3 - OFFSET, WIDTH // 3 - OFFSET))

