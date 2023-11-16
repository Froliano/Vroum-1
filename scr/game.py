import time

import pygame
from random import randint, choice
from car import Car
from player import Player
from coin import Coin
from bomb import Bomb
from init import WIDTH, HEIGHT


class Game:

    def __init__(self, screen, bestScore, coins, bombs, pieceSound, bombSound, carCollideSound):

        self.screen = screen
        self.pressed = {}
        self.speed = 10
        self.pieceSound = pieceSound
        self.bombSound = bombSound
        self.carCollideSound = carCollideSound

        self.score = 0
        self.gameOverbool = False
        self.close = False
        self.objects = []
        self.bombs = []

        self.bestScore = bestScore
        self.coins = coins
        self.numberBombs = bombs

        self.boumImage = pygame.image.load("./assets/boum.png")

        self.bombImage = pygame.image.load("./assets/bomb.png")
        self.bombImage = pygame.transform.scale(self.bombImage, (80, 80))

        self.coinsImages = []
        self.coinImages = pygame.image.load("./assets/coin.png")
        for x in range(0, self.coinImages.get_rect()[2], self.coinImages.get_rect()[2] // 13):
            self.coinsImages.append(self.getCoinImage(x, 0))

        self.carsImages = []
        self.carImages = pygame.image.load("./assets/cars.png")
        for x in range(0, self.carImages.get_rect()[2], self.carImages.get_rect()[2] // 3):
            for y in range(0, self.carImages.get_rect()[3]-1, self.carImages.get_rect()[3] // 2):
                self.carsImages.append(self.getCarImage(x, y))


        self.font = pygame.font.Font("./munro.ttf", 40)
        self.countdownFont = pygame.font.Font("./munro.ttf", 100)

        self.delay = 1
        self.cooldown = 0.8
        self.gameOverCooldown = 1.5
        self.timer = time.time()
        self.timecountdown = 3
        self.timercountdown = time.time()
        self.player = Player(1, choice(self.carsImages))
        self.left = True
        self.right = True
        self.space = True

        for i in range(self.numberBombs):
            self.bombs.append(Bomb(self.player.x, self.player.y, self.bombImage))

    def update(self):
        self.lines()

        if time.time() <= self.timercountdown + self.timecountdown:
            self.countdownText = self.countdownFont.render(f"{int((self.timercountdown + self.timecountdown) - time.time())+1}", True, "black")
            self.screen.blit(self.countdownText, (WIDTH//2 - self.countdownText.get_width()//2, HEIGHT//2 - self.countdownText.get_height()//2))
        else:
            self.input()
            self.addObject()
            self.delObject()

        if self.score >= (self.speed - 9) ** 2 * 1.5:
            self.speed += 1

        self.player.draw(self.screen)

        for object in self.objects:
            object.update(self.screen, self.speed)

        for bomb in self.bombs:
            bomb.update(self.screen)

        collision = self.player.collide(self.objects)
        if collision[0] == 1:
            self.objects.remove(collision[1])
            self.coins += 1
            pygame.mixer.Sound.play(self.pieceSound)
        elif collision[0] == 2:
            if not self.gameOverbool:
                self.gameOverTime = time.time()
                pygame.mixer.Sound.play(self.carCollideSound)
            self.carCollide = collision[1]
            self.gameOver()
        if len(self.bombs) > 0:
            bombCollision = self.bombs[0].collide(self.objects)
            if bombCollision[0] == 1:
                self.objects.remove(bombCollision[1])
                self.bombs.pop(0)

        self.numberBombsText = self.font.render(f"{self.numberBombs}", True, "white")
        self.screen.blit(self.bombImage, (10, 10))
        self.screen.blit(self.numberBombsText, (self.bombImage.get_rect()[2] + 20, 30))


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
                if self.space and len(self.bombs) > 0 and not self.bombs[0].lunch:
                    self.bombs[0].activeLunch()
                    self.numberBombs -= 1
                    self.space = False
                    pygame.mixer.Sound.play(self.bombSound)
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
        if time.time() > self.timer + self.cooldown:
            self.timer = time.time()
            if randint(1, 5) == 1:
                self.objects.append(Coin(self.coinsImages, randint(0, 2)))
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
        self.boom()
        if self.score > self.bestScore:
            self.bestScore = self.score
        if time.time() > self.gameOverTime + self.gameOverCooldown:
            self.close = True

    def getCarImage(self, x, y):
        image = pygame.Surface((self.carImages.get_rect()[2]//3-20, self.carImages.get_rect()[3]//2-10))
        image.blit(self.carImages, (0, 0), (x+10, y+5, self.carImages.get_rect()[2]//3-20, self.carImages.get_rect()[3]//2-10))
        image.set_colorkey([0, 0, 0])
        return image

    def getCoinImage(self, x, y):
        image = pygame.Surface((self.coinImages.get_rect()[2]//13, self.coinImages.get_rect()[3]))
        image.blit(self.coinImages, (0, 0), (x, y, self.coinImages.get_rect()[2]//13, self.coinImages.get_rect()[3]))
        image.set_colorkey([0, 0, 0])
        return image

    def boom(self):
        if self.player.y > self.carCollide.y:
            y = self.player.y - self.boumImage.get_rect()[3] // 2
        elif self.player.y < self.carCollide.y:
            y = self.player.y + self.boumImage.get_rect()[3] // 2

        self.screen.blit(self.boumImage, ((self.player.x * WIDTH//3) - self.boumImage.get_rect()[2] // 6, y))

    def buyBomb(self):
        if self.coins >= 3:
            self.numberBombs += 1
            self.coins -= 3
