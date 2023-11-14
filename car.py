import pygame
from init import WIDTH, OFFSET, CAR_SIZE

class Car:

    def __init__(self, x, y = -200, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.Rect((self.x * WIDTH // 3 + OFFSET // 2, self.y), CAR_SIZE)

    def update(self, screen, speed):
        self.draw(screen)
        self.fall(speed)

    def draw(self, screen):
        self.rect = pygame.Rect((self.x * WIDTH // 3 + OFFSET // 2, self.y), CAR_SIZE)
        pygame.draw.rect(screen, self.color, self.rect)

    def fall(self, speed):
        self.y += speed

    def getRect(self):
        return pygame.rect

