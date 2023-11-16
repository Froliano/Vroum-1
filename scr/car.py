import pygame
from random import randint
from init import WIDTH, OFFSET, CAR_SIZE

class Car:

    def __init__(self, image, x, y = -200):
        # caracteristiques de la voiture
        self.x = x
        self.y = y
        self.rect = pygame.Rect((self.x * WIDTH // 3 + OFFSET // 2, self.y), CAR_SIZE)

        # gestion de l'image
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.rect[2], self.rect[3]))
        self.image = pygame.transform.rotate(self.image, 180)

        # acceleration de la voiture de maniere aleatoire
        self.acceleration = randint(1, 20)
        if self.acceleration < 12:
            self.acceleration = 1
        elif self.acceleration < 20:
            self.acceleration = 2
        else:
            self.acceleration = 3

    def update(self, screen, speed):
        """
        methode appelee en boucle pour chaque voiture
        """
        self.draw(screen)
        self.fall(speed)

    def draw(self, screen):
        """
        calculer le rect de la voiture (position et taille),
            le numero de la ligne * 1/3 de la taille de l'ecran + un decalage pour centrer la voiture
        dessiner la bombe sur le screen a la place voulue
        """
        self.rect = pygame.Rect((self.x * WIDTH // 3 + OFFSET // 2, self.y), CAR_SIZE)
        screen.blit(self.image, (self.x * WIDTH // 3 + OFFSET // 2, self.y))
        #pygame.draw.rect(screen, self.color, self.rect)

    def fall(self, speed):
        """
        mouvement des voitures qui arrivent sur le joueur en fonction de la speed
        """
        self.y += speed * self.acceleration

    def getRect(self):
        return self.rect

