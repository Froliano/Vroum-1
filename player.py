import pygame
from coin import Coin
from car import Car
from init import CAR_SIZE, HEIGHT, WIDTH, OFFSET


class Player:

    def __init__(self, x):
        self.x = x
        self.y = HEIGHT//1.5
        self.rect = pygame.Rect((self.x*WIDTH//3 + OFFSET//2, self.y), CAR_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, "blue", pygame.Rect((self.x*WIDTH//3 + OFFSET//2, self.y ), CAR_SIZE))

    def left(self):
        if self.x != 0:
            self.x -= 1
            self.rect = pygame.Rect((self.x * WIDTH // 3 + OFFSET // 2, self.y), CAR_SIZE)

    def right(self):
        if self.x != 2:
            self.x += 1
            self.rect = pygame.Rect((self.x * WIDTH // 3 + OFFSET // 2, self.y), CAR_SIZE)

    def collide(self, objects):

        for object in objects:
            if pygame.Rect.colliderect(object.getRect(), self.rect):
                if type(object) is Coin:
                    return (1, object)
                else:
                    return (2, 0)
        return (0, 0)