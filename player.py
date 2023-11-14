import pygame
from coin import Coin
from car import Car
from init import CAR_SIZE, HEIGHT, WIDTH, OFFSET


class Player:

    def __init__(self, x):
        self.x = x
        self.rect = pygame.Rect((self.x*WIDTH//3 + OFFSET//2, HEIGHT//2), CAR_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, "blue", pygame.Rect((self.x*WIDTH//3 + OFFSET//2, HEIGHT//2), CAR_SIZE))

    def left(self):
        if self.x != 0:
            self.x -= 1
            self.rect = pygame.Rect((self.x * WIDTH // 3 + OFFSET // 2, HEIGHT // 2), CAR_SIZE)

    def right(self):
        if self.x != 2:
            self.x += 1
            self.rect = pygame.Rect((self.x * WIDTH // 3 + OFFSET // 2, HEIGHT // 2), CAR_SIZE)

    def collide(self, objects):

        for objet in objects:
            if pygame.Rect.colliderect(objet.getRect(), self.rect):
                if type(objet) is Coin:
                    return 1
                else:
                    return 2
        return 0