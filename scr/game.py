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

        # caracteristiques du jeu
        self.screen = screen
        self.pressed = {}
        self.speed = 10

        # initialisation des sons
        self.pieceSound = pieceSound
        self.bombSound = bombSound
        self.carCollideSound = carCollideSound

        # initialisation des variables
        self.score = 0
        self.gameOverBool = False
        self.close = False
        self.objects = []
        self.bombs = []

        # initialisation des variable qui seront sauvegardees
        self.bestScore = bestScore
        self.coins = coins
        self.numberBombs = bombs

        # initialisation des variables temporelles
        self.linesDelay = 1
        self.gameOverCooldown = 1.5

        self.objectCooldown = 0.8
        self.objectTimer = time.time()

        self.timecountdown = 3
        self.timercountdown = time.time()

        # chargement des images
        self.boumImage = pygame.image.load("../assets/boum.png")
        self.bombImage = pygame.image.load("../assets/bomb.png")
        self.bombImage = pygame.transform.scale(self.bombImage, (80, 80))

        # chargement et decoupage des images de la piece
        self.coinsImages = []
        self.coinImages = pygame.image.load("../assets/coin.png")
        for x in range(0, self.coinImages.get_rect()[2], self.coinImages.get_rect()[2] // 13):
            self.coinsImages.append(self.getCoinImage(x, 0))

        # chargement et decoupage des images des voitures
        self.carsImages = []
        self.carImages = pygame.image.load("../assets/cars.png")
        for x in range(0, self.carImages.get_rect()[2], self.carImages.get_rect()[2] // 3):
            for y in range(0, self.carImages.get_rect()[3]-1, self.carImages.get_rect()[3] // 2):
                self.carsImages.append(self.getCarImage(x, y))

        # initialisation de la police
        self.font = pygame.font.Font("../munro.ttf", 40)
        self.countdownFont = pygame.font.Font("../munro.ttf", 100)


        # initialisation du joueur
        self.player = Player(1, choice(self.carsImages))

        # initialisation des booleens permettant aux inputs une simple pression
        self.left = True
        self.right = True
        self.space = True

        # ajout du nombre de bombes dans la liste des bombes
        for i in range(self.numberBombs):
            self.bombs.append(Bomb(self.player.x, self.player.y, self.bombImage))

    def update(self):
        self.lines()
        """
        mise en place du systeme de compte a rebours
            affichage du timer 
            bloquer les inputs et les ajouts d'objets pendant le compte a rebours
        """
        if time.time() <= self.timercountdown + self.timecountdown:
            self.countdownText = self.countdownFont.render(f"{int((self.timercountdown + self.timecountdown) - time.time())+1}", True, "black")
            self.screen.blit(self.countdownText, (WIDTH//2 - self.countdownText.get_width()//2, HEIGHT//2 - self.countdownText.get_height()//2))
        else:
            self.input()
            self.addObject()
            self.delObject()

        # augmentation de la vitesse en fonction du score avec la formule x² * 1.5
        if self.score >= (self.speed - 9) ** 2 * 1.5:
            self.speed += 1

        # affichage du joueur
        self.player.draw(self.screen)

        # update de tous les objets present dans la map
        for object in self.objects:
            object.update(self.screen, self.speed)

        # update de toutes les bombes present dans la map
        for bomb in self.bombs:
            bomb.update(self.screen)


        # verification des collision
        collision = self.player.collide(self.objects)

        # si il y a une collision entre le joueur et une piece
        # supprimer la piece des objet de la map et ajouter une piece au compteur
        if collision[0] == 1:
            self.objects.remove(collision[1])
            self.coins += 1
            pygame.mixer.Sound.play(self.pieceSound)

        # si il y a une collision entre le joueur et une voiture
        # mise en place du cooldown du game over et appel de game over
        elif collision[0] == 2:
            if not self.gameOverBool:
                self.gameOverTime = time.time()
                pygame.mixer.Sound.play(self.carCollideSound)
            self.carCollide = collision[1]
            self.gameOver()

        # si le joueur a une bombe et quelle est en collision avec une voiture
        # supprimer la bombe et la voiture touchee
        if len(self.bombs) > 0:
            bombCollision = self.bombs[0].collide(self.objects)
            if bombCollision[0] == 1:
                self.objects.remove(bombCollision[1])
                self.bombs.pop(0)

        # affichage du nombre de bombe
        self.numberBombsText = self.font.render(f"{self.numberBombs}", True, "white")
        self.screen.blit(self.bombImage, (10, 10))
        self.screen.blit(self.numberBombsText, (self.bombImage.get_rect()[2] + 20, 30))


        # affichage du score
        self.scoreText = self.font.render(f"score : {self.score}", True, "white")
        self.scoreTextRect = self.scoreText.get_rect()
        self.scoreTextRect.topright = (WIDTH -10, 10)
        self.screen.blit(self.scoreText, (self.scoreTextRect.topright[0] - self.scoreTextRect.w, self.scoreTextRect.topright[1]))

        # affichage du nombre de pieces
        self.coinText = self.font.render(f"coins : {self.coins}", True, "white")
        self.coinTextRect = self.coinText.get_rect()
        self.coinTextRect.topright = (WIDTH - 10, 50)
        self.screen.blit(self.coinText, (self.coinTextRect.topright[0] - self.coinTextRect.w, self.coinTextRect.topright[1]))

    def input(self):
        # verifier si le jeu est en cours
        if not self.gameOverBool:

            # recuperer l'input de la fleche gauche et deplacer le joueur
            if self.pressed.get(pygame.K_LEFT):
                if self.left:
                    self.player.left()
                    for bomb in self.bombs:
                        bomb.left()
                    self.left = False
            else:
                self.left = True

            # recuperer l'input de la fleche droite et deplacer le joueur
            if self.pressed.get(pygame.K_RIGHT):
                if self.right:
                    self.player.right()
                    for bomb in self.bombs:
                        bomb.right()
                    self.right = False
            else:
                self.right = True

            # recupere l'input espace pour envoyer la bombe si le joueur en possede et qu'aucune bombe est lancee
            if self.pressed.get(pygame.K_SPACE):
                if self.space and len(self.bombs) > 0 and not self.bombs[0].lunch:
                    self.bombs[0].activeLunch()
                    self.numberBombs -= 1
                    self.space = False
                    pygame.mixer.Sound.play(self.bombSound)
            else:
                self.space = True

    def lines(self):
        # dessin des deux ligne blanche sur la map
        pygame.draw.rect(self.screen, "white", pygame.Rect(WIDTH // 3 - 5, 0, 10, HEIGHT))
        pygame.draw.rect(self.screen, "white", pygame.Rect((WIDTH // 3) * 2 - 5, 0, 10, HEIGHT))

        # dessin des petites ligne gris a intervalle reguliere et sur tout l'ecran
        # pour donner l'impression que la ligne blanche est coupee
        for i in range(-100+self.linesDelay, HEIGHT+self.linesDelay, 80):
            pygame.draw.rect(self.screen, (128, 129, 129), pygame.Rect(WIDTH // 3 - 5, i, 10, 50))
            pygame.draw.rect(self.screen, (128, 129, 129), pygame.Rect((WIDTH // 3) * 2 - 5, i, 10, 50))
        self.linesDelay = (self.linesDelay + self.speed) % 80

    def addObject(self):
        """
        ajout a intervalle reguliere d'un objet aleatoirement entre une piece et une voiture
            a une position x aleatoire entre 0 et 2
        """
        if time.time() > self.objectTimer + self.objectCooldown:
            self.objectTimer = time.time()
            if randint(1, 3) == 1:
                self.objects.append(Coin(self.coinsImages, randint(0, 2)))
            else:
                self.objects.append(Car(choice(self.carsImages), randint(0, 2)))


    def delObject(self):
        """
        si il y a des objets sur la map verifier si ils sont sortis de l'ecran pour les supprimer
            ajout d'un point si l'objet est une voiture
        suppression d'une bombe si la liste des bombe est pas vide et si une bombe sort de l'ecran
        :return:
        """
        if len(self.objects) > 0:
            if self.objects[0].y > HEIGHT+200:
                if type(self.objects[0]) is Car:
                    self.score += 1
                self.objects.pop(0)
        if len(self.bombs) > 0 and self.bombs[0].y < -50:
            self.bombs.pop(0)

    def setPressed(self, pressed):
        """
        recuperer les inputs du joueur
        """
        self.pressed = pressed

    def gameOver(self):
        """
        methode pour mettre fin au jeu en mettant la vitesse du jeu a 0 et en affichant l'image boom1
        calcul du meilleur score de toutes les games
        fermeture du jeu apres un certain delay
        """
        self.gameOverBool = True
        self.speed = 0
        self.boom()
        if self.score > self.bestScore:
            self.bestScore = self.score
        if time.time() > self.gameOverTime + self.gameOverCooldown:
            self.close = True

    def getCarImage(self, x, y):
        """
        decoupage et recuperation d'une voiture a partir d'une image de plusieurs voiture
        """
        image = pygame.Surface((self.carImages.get_rect()[2]//3-20, self.carImages.get_rect()[3]//2-10))
        image.blit(self.carImages, (0, 0), (x+10, y+5, self.carImages.get_rect()[2]//3-20, self.carImages.get_rect()[3]//2-10))
        image.set_colorkey([0, 0, 0])
        return image

    def getCoinImage(self, x, y):
        """
        decoupage et recuperation d'une image de l'animation d'une piece a partir d'une image de plusieurs
            position d'animation d'une piece
        """
        image = pygame.Surface((self.coinImages.get_rect()[2]//13, self.coinImages.get_rect()[3]))
        image.blit(self.coinImages, (0, 0), (x, y, self.coinImages.get_rect()[2]//13, self.coinImages.get_rect()[3]))
        image.set_colorkey([0, 0, 0])
        return image

    def boom(self):
        """
        verifier si la position du joueur en y est plus grande ou plus petite que la voiture en collision
        affichage de boum a la position de la collision
        """
        if self.player.y > self.carCollide.y:
            y = self.player.y - self.boumImage.get_rect()[3] // 2
        else:
            y = self.player.y + self.boumImage.get_rect()[3] // 2

        self.screen.blit(self.boumImage, ((self.player.x * WIDTH//3) - self.boumImage.get_rect()[2] // 6, y))