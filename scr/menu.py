import pygame

from button import Button

class Menu:

    def __init__(self, screen, bg):
        # caracteristique du menu
        self.screen = screen
        self.bg = bg
        self.buttons = []
        self.labels = []

        # changement de la police
        self.font = pygame.font.Font("../munro.ttf", 50)

    def update(self):
        """
        methode appelee en boucle pour afficher tout les elements du menu
        background, boutons, label
        """
        self.screen.blit(self.bg, (0, 0))

        for button in self.buttons:
            button.draw()

        for label in self.labels:
            self.screen.blit(label[0], label[1])


    def addButton(self, id, x, y, w, h, image, text, size, color):
        """
        ajout d'un bouton de classe Button avec ses coordonnees, sa taille, son image de fond, son text
            sa police et sa couleur
        """
        self.font = pygame.font.Font("../munro.ttf", size)
        self.buttons.append(Button(id, x, y, w, h, image, self.screen, text, self.font, color))

    def addLabel(self, x, y, text, size, color, id):
        """
        ajout d'un label avec ses coordonnees, son text et la taille de sa police
        """
        self.font = pygame.font.Font("../munro.ttf", size)
        self.labels.append((self.font.render(text, True, color), (x,y), id))

    def updateLabel(self, x, y, text, size, color, id):
        """
        mise a jour d'un label en fonction de l'id pour changer le texte
        suppression du label avec l'identifiant id puis creation d'un nouveau label
        """
        for label in self.labels:
            if label[2] == id:
                self.font = pygame.font.Font("../munro.ttf", size)
                self.labels.append((self.font.render(text, True, color), (x, y), id))
                self.labels.remove(label)

    def collide(self, x, y):
        """
        :param x: position x de la sourie
        :param y: position y de la souris
        verifie la collision entre la souris et tout les boutons du menu
        :return: booleen, si la souris est en contact avec le bouton au moment du click
            et id du bouton collisionne
        """
        for button in self.buttons:
            if button.collide(x, y):
                return (True,button.id)
        return (False, 0)
