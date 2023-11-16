import pygame

from button import Button

class Menu:

    def __init__(self, screen, bg):
        self.screen = screen
        self.bg = bg

        self.font = pygame.font.Font("./munro.ttf", 50)
        self.buttons = []
        self.labels = []

    def update(self):
        self.screen.blit(self.bg, (0, 0))

        for button in self.buttons:
            button.draw()

        for label in self.labels:
            self.screen.blit(label[0], label[1])


    def addButton(self, id, x, y, w, h, image, text, size, color):
        self.font = pygame.font.Font("./munro.ttf", size)
        self.buttons.append(Button(id, x, y, w, h, image, self.screen, text, self.font, color))

    def addLabel(self, x, y, text, size, color, id):
        self.font = pygame.font.Font("./munro.ttf", size)
        self.labels.append((self.font.render(text, True, color), (x,y), id))

    def updateLabel(self, x, y, text, size, color, id):
        for label in self.labels:
            if label[2] == id:
                self.font = pygame.font.Font("./munro.ttf", size)
                self.labels.append((self.font.render(text, True, color), (x, y), id))
                self.labels.remove(label)

    def collide(self, x, y):
        for button in self.buttons:
            if button.collide(x, y):
                return (True,button.id)
        return (False, 0)
