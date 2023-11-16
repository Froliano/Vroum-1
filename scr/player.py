import pygame
from coin import Coin
from init import CAR_SIZE, HEIGHT, WIDTH, OFFSET


class Player:

    def __init__(self, x, image):
        # caracteristique du joueur
        self.x = x
        self.y = HEIGHT//1.5
        self.rect = pygame.Rect((self.x*WIDTH//3 + OFFSET//2, self.y), CAR_SIZE)

        # gestion de l'image du joueur
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.rect[2], self.rect[3]))


    def draw(self, screen):
        """
        affichage de l'image du joueur sur le screen a sa position
        """
        #pygame.draw.rect(screen, "blue", pygame.Rect((self.x*WIDTH//3 + OFFSET//2, self.y ), CAR_SIZE))
        screen.blit(self.image, (self.x*WIDTH//3 + OFFSET//2, self.y))

    def left(self):
        """
        deplacement du joueur vers la gauche pour si il le peut
        calcul de la nouvelle position du joueur
        """
        if self.x != 0:
            self.x -= 1
            self.rect = pygame.Rect((self.x * WIDTH // 3 + OFFSET // 2, self.y), CAR_SIZE)

    def right(self):
        """
        deplacement du joueur vers la droite pour si il le peut
        calcul de la nouvelle position du joueur
        """
        if self.x != 2:
            self.x += 1
            self.rect = pygame.Rect((self.x * WIDTH // 3 + OFFSET // 2, self.y), CAR_SIZE)

    def collide(self, objects):
        """
        verification et identification de la collision entre la joueur et un objet avec le 1er element du tuple
            1 si il s'agit d'une piece et 2 si il s'agit d'une voiture
        renvoi de l'objet entree en collision avec le joueur
        """

        for object in objects:
            if pygame.Rect.colliderect(object.getRect(), self.rect):
                if type(object) is Coin:
                    return (1, object)
                else:
                    return (2, object)
        return (0, 0)