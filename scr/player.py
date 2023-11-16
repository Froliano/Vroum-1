import pygame
from coin import Coin
from car import Car
from init import CAR_SIZE, HEIGHT, WIDTH, OFFSET


class Player:

    def __init__(self, x, image):
        self.x = x
        self.y = HEIGHT//1.5
        self.rect = pygame.Rect((self.x*WIDTH//3 + OFFSET//2, self.y), CAR_SIZE)

        self.image = image
        self.image = pygame.transform.scale(self.image, (self.rect[2], self.rect[3]))


    def draw(self, screen):
        #pygame.draw.rect(screen, "blue", pygame.Rect((self.x*WIDTH//3 + OFFSET//2, self.y ), CAR_SIZE))
        screen.blit(self.image, (self.x*WIDTH//3 + OFFSET//2, self.y))

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
                    return (2, object)
        return (0, 0)