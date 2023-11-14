import pygame

from init import WIDTH

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
        pygame.draw.circle(screen, "yellow", self.rectCenter, 50)

    def fall(self, speed):
        self.y += speed

    def addCoin(self, coins):
        coins += 1

    def getRect(self):
        print(pygame.Rect((self.rectCenter[0]-50, self.rectCenter[1]-50), 100, 100))
        return pygame.Rect((self.rectCenter[0]-50, self.rectCenter[1]-50), 100, 100)

