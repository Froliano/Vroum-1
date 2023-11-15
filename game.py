import time

import pygame
from random import randint, choice

from car import Car
from player import Player
from coin import Coin
from bomb import Bomb
from init import WIDTH, HEIGHT


class Game:

    def __init__(self, screen, bestScore, coins):

        self.screen = screen
        self.pressed = {}
        self.speed = 10

        self.bestScore = bestScore
        self.score = 0
        self.coins = coins
        self.gameOverbool = False

        self.coinsImages = []
        self.coinImages = pygame.image.load("coin.png")
        for x in range(0, self.coinImages.get_rect()[2], self.coinImages.get_rect()[2] // 13):
            self.coinsImages.append(self.getCoinImage(x, 0))


        self.carsImages = []
        self.carImages = pygame.image.load("cars.png")
        for x in range(0, self.carImages.get_rect()[2], self.carImages.get_rect()[2] // 3):
            for y in range(0, self.carImages.get_rect()[3]-1, self.carImages.get_rect()[3] // 2):
                self.carsImages.append(self.getCarImage(x, y))

                #print(y, self.images.get_rect()[3], self.images.get_rect()[3] // 2)



        self.objects = []
        self.player = Player(0, choice(self.carsImages))
        self.numberBombs = 4
        self.bombs = []

        self.font = pygame.font.Font("munro.ttf", 40)

        self.delay = 0
        self.cooldown = 0.8
        self.timer = time.time()
        self.left = True
        self.right = True
        self.space = True

        for i in range(self.numberBombs):
            self.bombs.append(Bomb(self.player.x, self.player.y))

    def update(self):
        self.input()
        self.lines()

        self.addObject()
        self.delObject()

        collision = self.player.collide(self.objects)
        if collision[0] == 1:
            self.objects.remove(collision[1])
            self.coins += 1
        elif collision[0] == 2:
            self.gameOver()
        if len(self.bombs) > 0:
            bombCollision = self.bombs[0].collide(self.objects)
            if bombCollision[0] == 1:
                self.objects.remove(bombCollision[1])
                self.bombs.pop(0)

        if self.score >= (self.speed - 9) ** 2 * 1.5:
            self.speed += 1

        self.player.draw(self.screen)

        for object in self.objects:
            object.update(self.screen, self.speed)

        for bomb in self.bombs:
            bomb.update(self.screen)



        self.scoreText = self.font.render(f"score : {self.score}", True, "white")
        self.scoreTextRect = self.scoreText.get_rect()
        self.scoreTextRect.topright = (WIDTH -10, 10)
        self.screen.blit(self.scoreText, (self.scoreTextRect.topright[0] - self.scoreTextRect.w, self.scoreTextRect.topright[1]))

        self.coinText = self.font.render(f"coins : {self.coins}", True, "white")
        self.coinTextRect = self.coinText.get_rect()
        self.coinTextRect.topright = (WIDTH - 10, 50)
        self.screen.blit(self.coinText, (self.coinTextRect.topright[0] - self.coinTextRect.w, self.coinTextRect.topright[1]))

    def input(self):
        if not self.gameOverbool:
            if self.pressed.get(pygame.K_LEFT):
                if self.left:
                    self.player.left()
                    for bomb in self.bombs:
                        bomb.left()
                    self.left = False
            else:
                self.left = True

            if self.pressed.get(pygame.K_RIGHT):
                if self.right:
                    self.player.right()
                    for bomb in self.bombs:
                        bomb.right()
                    self.right = False
            else:
                self.right = True

            if self.pressed.get(pygame.K_SPACE):
                if self.space and len(self.bombs) > 0:
                    self.bombs[0].activeLunch()
                    self.space = False
            else:
                self.space = True

    def lines(self):
        pygame.draw.rect(self.screen, "white", pygame.Rect(WIDTH // 3 - 5, 0, 10, HEIGHT))
        pygame.draw.rect(self.screen, "white", pygame.Rect((WIDTH // 3) * 2 - 5, 0, 10, HEIGHT))

        for i in range(-100+self.delay, HEIGHT+self.delay, 80):
            pygame.draw.rect(self.screen, (128, 129, 129), pygame.Rect(WIDTH // 3 - 5, i, 10, 50))
            pygame.draw.rect(self.screen, (128, 129, 129), pygame.Rect((WIDTH // 3) * 2 - 5, i, 10, 50))
        self.delay = (self.delay + self.speed) % 80

    def addObject(self):
        if randint(1, 3) == 1 and time.time() > self.timer + self.cooldown:
            self.timer = time.time()
            if randint(1, 5) == 1:
                self.objects.append(Coin(randint(0, 2)))
            else:
                self.objects.append(Car(choice(self.carsImages), randint(0, 2)))


    def delObject(self):
        if len(self.objects) > 0:
            if self.objects[0].y > HEIGHT+200:
                if type(self.objects[0]) is Car:
                    self.score += 1
                self.objects.pop(0)
        if len(self.bombs) > 0 and self.bombs[0].y < 0:
            self.bombs.pop(0)

    def setPressed(self, pressed):
        self.pressed = pressed

    def gameOver(self):
        self.gameOverbool = True
        self.speed = 0
        if self.score > self.bestScore:
            self.bestScore = self.score

    def getCarImage(self, x, y):
        image = pygame.Surface((self.carImages.get_rect()[2]//3-20, self.carImages.get_rect()[3]//2-10))
        image.blit(self.carImages, (0, 0), (x+10, y+5, self.carImages.get_rect()[2]//3-20, self.carImages.get_rect()[3]//2-10))
        image.set_colorkey([0, 0, 0])
        return image

    def getCoinImage(self, x, y):
        image = pygame.Surface((self.coinImages.get_rect()[2]//3-20, self.coinImages.get_rect()[3]//2-10))
        image.blit(self.coinImages, (0, 0), (x+10, y+5, self.coinImages.get_rect()[2]//3-20, self.coinImages.get_rect()[3]//2-10))
        image.set_colorkey([0, 0, 0])
        return image

