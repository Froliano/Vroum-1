import pygame

from random import randint
from init import WIDTH, OFFSET

class Coin:

    def __init__(self, images, x, y = -200):
        self.x = x
        self.y = y

        self.images = images
        self.currentImage = 0
        self.image = self.images[self.currentImage]
        self.image = pygame.transform.scale(self.image, (WIDTH // 6, WIDTH // 6))

        self.rectCenter = (self.x * WIDTH // 3 + WIDTH // 6, self.y)

    def update(self, screen, speed):
        self.draw(screen)
        self.fall(speed)
        self.animate()

    def draw(self, screen):
        self.rectCenter = (self.x * WIDTH // 3 + WIDTH // 6, self.y)
        screen.blit(self.image, (self.rectCenter[0] - WIDTH // 12, self.rectCenter[1]))
        #pygame.draw.circle(screen, "yellow", self.rectCenter, WIDTH // 6 - OFFSET // 2)

    def fall(self, speed):
        self.y += speed

    def animate(self):
        if randint(1, 2) == 1:
            if self.currentImage < len(self.images)-1:
                self.currentImage += 1
            else:
                self.currentImage = 0
            self.image = self.images[self.currentImage]
            self.image = pygame.transform.scale(self.image, (WIDTH // 6, WIDTH // 6))

    def getRect(self):
        return pygame.Rect((self.rectCenter[0]- OFFSET // 2, self.rectCenter[1]- OFFSET // 2), (WIDTH // 3 - OFFSET, WIDTH // 3 - OFFSET))

