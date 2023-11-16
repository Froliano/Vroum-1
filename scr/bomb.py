import pygame

from car import Car
from init import WIDTH, OFFSET


class Bomb:

    def __init__(self, x, y, image):
        # caracteristique de la bombe
        self.x = x
        self.y = y
        self.speed = 10
        self.lunch = False
        self.rectCenter = (self.x * WIDTH // 3 + WIDTH // 6, self.y)

        # gestion de l'image de la bombe
        self.image = image
        self.image = pygame.transform.scale(self.image, (WIDTH // 6, WIDTH // 6))

    def update(self, screen):
        """
        methode appelee en boucle quand la bombe est lancee
        """
        if self.lunch:
            self.draw(screen)
            self.move()

    def draw(self, screen):
        """
        calculer le centre de la ligne dans laquelle se situe la bombe
        dessiner la bombe sur le screen a la place voulue
        """
        self.rectCenter = (self.x * WIDTH // 3 + WIDTH // 6, self.y)
        screen.blit(self.image, (self.rectCenter[0] - WIDTH // 12, self.rectCenter[1]))
        #pygame.draw.circle(screen, "black", self.rectCenter, WIDTH // 6 - OFFSET)

    def activeLunch(self):
        """
        activer le booleen de lancement de la bombe
        """
        self.lunch = True

    def collide(self, objects):
        """
        quand la bombe est lancee verifier si elle est en contact avec toute les
        voiture presente sur le terrain
        :return tuple avec l'element 1 qui represente le booleen et l'element 2 qui renvoie l'objet à supprimer
        """
        if self.lunch:
            for object in objects:
                if type(object) is Car:
                    if pygame.Rect.colliderect(object.getRect(), self.getRect()):
                        return (1, object)
            return (0, 0)
        return (0, 0)


    def left(self):
        """
        deplacement de la bombe vers la gauche pour suivre les mouvement du joueur avant que la bombe ne soit lancee
        calcul du centre de la position de la bombe
        """
        if self.x != 0 and not self.lunch:
            self.x -= 1
            self.rectCenter = (self.x * WIDTH // 3 + WIDTH // 6, self.y)

    def right(self):
        """
        deplacement de la bombe vers la droite pour suivre les mouvement du joueur avant que la bombe ne soit lancee
        calcul du centre de la position de la bombe
        """
        if self.x != 2 and not self.lunch:
            self.x += 1
            self.rectCenter = (self.x * WIDTH // 3 + WIDTH // 6, self.y)

    def move(self):
        self.y -= self.speed

    def getRect(self):
        return pygame.Rect((self.rectCenter[0] - OFFSET // 2, self.rectCenter[1] - OFFSET // 4), (WIDTH // 3 - 2*OFFSET, WIDTH // 3 - 2*OFFSET))