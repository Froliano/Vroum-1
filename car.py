import pygame
from random import randint
from init import WIDTH, OFFSET, CAR_SIZE

class Car:

    def __init__(self, x, y = -200, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.Rect((self.x * WIDTH // 3 + OFFSET // 2, self.y), CAR_SIZE)
        self.acceleration = randint(1, 10)
        if self.acceleration < 6:
            self.acceleration = 1
        elif self.acceleration < 10:
            self.acceleration = 2
        else:
            self.acceleration = 3

    def update(self, screen, speed):
        self.draw(screen)
        self.fall(speed)

    def draw(self, screen):
        self.rect = pygame.Rect((self.x * WIDTH // 3 + OFFSET // 2, self.y), CAR_SIZE)
        pygame.draw.rect(screen, self.color, self.rect)

    def fall(self, speed):
        self.y += speed * self.acceleration

    def getRect(self):
        return self.rect

