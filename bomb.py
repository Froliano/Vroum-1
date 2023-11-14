import pygame

from car import Car
from init import WIDTH, OFFSET

class Bomb:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.lunch = False

    def update(self, screen):
        if self.lunch:
            self.draw(screen)
            self.move()

    def draw(self, screen):
        self.rectCenter = (self.x * WIDTH // 3 + WIDTH // 6, self.y)
        pygame.draw.circle(screen, "black", self.rectCenter, WIDTH // 6 - OFFSET)

    def activeLunch(self):
        self.lunch = True

    def collide(self, objects):
        if self.lunch:
            for object in objects:
                if type(object) is Car:
                    if pygame.Rect.colliderect(object.getRect(), self.getRect()):
                        return (1, object)
            return (0, 0)
        return (0, 0)


    def left(self):
        if self.x != 0 and not self.lunch:
            self.x -= 1
            self.rectCenter = (self.x * WIDTH // 3 + WIDTH // 6, self.y)

    def right(self):
        if self.x != 2 and not self.lunch:
            self.x += 1
            self.rectCenter = (self.x * WIDTH // 3 + WIDTH // 6, self.y)

    def move(self):
        self.y -= self.speed

    def getRect(self):
        return pygame.Rect((self.rectCenter[0] - OFFSET // 2, self.rectCenter[1] - OFFSET // 4), (WIDTH // 3 - 2*OFFSET, WIDTH // 3 - 2*OFFSET))