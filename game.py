import pygame
from random import randint

from car import Car
from player import Player
from coin import Coin
from init import WIDTH, HEIGHT

coin = Coin(2, 100)
class Game:

    def __init__(self, screen):

        self.screen = screen
        self.pressed = {}
        self.speed = 10

        self.score = 0
        self.coins = 0

        self.objects = []
        #self.objects.append(coin)
        self.player = Player(0)

        self.delay = 0
        self.left = True
        self.right = True

    def update(self):
        self.lines()
        self.input()

        self.addObject()
        self.delObject()

        collision = self.player.collide(self.objects)
        if collision == 1:
            print("piece")
        elif collision == 2:
            self.speed = 0

        self.player.draw(self.screen)
        if self.score >= (self.speed - 9) ** 2 * 1.5:
            self.speed += 1

        for object in self.objects:
            object.update(self.screen, self.speed)

    def input(self):

        if self.pressed.get(pygame.K_LEFT):
            if self.left:
                self.player.left()
                self.left = False
        else:
            self.left = True

        if self.pressed.get(pygame.K_RIGHT):
            if self.right:
                self.player.right()
                self.right = False
        else:
            self.right = True

    def lines(self):
        pygame.draw.rect(self.screen, "white", pygame.Rect(WIDTH // 3 - 5, 0, 10, HEIGHT))
        pygame.draw.rect(self.screen, "white", pygame.Rect((WIDTH // 3) * 2 - 5, 0, 10, HEIGHT))

        for i in range(-100+self.delay, HEIGHT+self.delay, 80):
            pygame.draw.rect(self.screen, (128, 129, 129), pygame.Rect(WIDTH // 3 - 5, i, 10, 50))
            pygame.draw.rect(self.screen, (128, 129, 129), pygame.Rect((WIDTH // 3) * 2 - 5, i, 10, 50))
        self.delay = (self.delay + self.speed) % 80

    def addObject(self):
        if randint(1, 50) == 1 and len(self.objects) < 2:
            self.objects.append(Car(randint(0, 2)))
            for i in range(3):
                a = 0
                for object in self.objects:
                    if object.x == i:
                        if a == 1:
                            self.objects.remove(object)
                        a += 1

    def delObject(self):
        if len(self.objects) > 0:
            if self.objects[0].y > HEIGHT+200:
                self.objects.pop(0)
                if type(object) is Car:
                    self.score += 1

    def setPressed(self, pressed):
        self.pressed = pressed

