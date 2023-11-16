import pygame

from game import Game
from menu import Menu
from init import WIDTH, HEIGHT

pygame.init()

def main():
    # creation de la fenetre et de ses caracteristiques
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("VROUM 1")
    lambo = pygame.image.load("../assets/lambo.png").convert()
    pygame.display.set_icon(lambo)

    # caracteristique du jeu
    timer = pygame.time.Clock()
    fps = 60
    window = "menu"

    # recuperation des donnees sauvegardes
    bestScore, coins, bombs = getSave()

    # initialisation des booleens permettant aux inputs une simple pression
    mouseClick = False

    # changement des musiques et sons du jeu
    mainMusic = pygame.mixer.Sound("../sounds/mainMusic.mp3")
    buttonSound = pygame.mixer.Sound("../sounds/clickButton.mp3")
    pieceSound = pygame.mixer.Sound("../sounds/piece.wav")
    launchBombSound = pygame.mixer.Sound("../sounds/launchBomb.mp3")
    carCollideSound = pygame.mixer.Sound("../sounds/carCollide.mp3")

    # chargement des images du menu principal
    bgMainMenu = pygame.image.load("../assets/bgMenu.png")
    bgMainMenu = pygame.transform.scale(bgMainMenu, (WIDTH, HEIGHT))
    mainMenuButtonImage = pygame.image.load("../assets/greenButton.png")

    # creation du menu principal
    mainMenu = Menu(screen, bgMainMenu)
    mainMenu.addLabel(WIDTH//2 - 150, HEIGHT //12, "VROUM 1", 100, "blue", 0)
    mainMenu.addLabel(WIDTH//2 - 175, (HEIGHT //6)*1.5, f"Best Score: {bestScore}", 70, "Blue", 1)
    mainMenu.addButton(0, WIDTH//2 - 100, (HEIGHT //3)*1.5, 200, 70, mainMenuButtonImage, "PLAY", 50, "Blue")
    mainMenu.addButton(1, WIDTH//2 - 100, (HEIGHT //3)*2, 200, 70, mainMenuButtonImage, "SHOP", 50, "Blue")
    mainMenu.addButton(2, WIDTH//2 - 100, (HEIGHT //3)*2.5, 200, 70, mainMenuButtonImage, "EXIT", 50, "Blue")

    # chargement des images du menu shop
    bgShopMenu = pygame.image.load("../assets/shopBG.png")
    bgShopMenu = pygame.transform.scale(bgShopMenu, (WIDTH, HEIGHT))
    shopMenuButtonImage = pygame.image.load("../assets/redButton.png")
    shopMenuinfoImage = pygame.image.load("../assets/goldButton.png")

    # creation du menu shop
    shopMenu = Menu(screen, bgShopMenu,)
    shopMenu.addLabel(WIDTH//2 - 80, HEIGHT //12, "SHOP", 100, "white", 2)
    shopMenu.addButton(5,50, (HEIGHT // 3) - 50, 400, 150, shopMenuinfoImage, "", 50, "black")
    shopMenu.addLabel(80, HEIGHT //3 - 40, f"coins : {coins}", 50, "black", 3)
    shopMenu.addLabel(80, HEIGHT //3 + 20, f"bombs : {bombs}", 50, "black", 4)
    shopMenu.addButton(3,50, (HEIGHT // 3) + 120 , 400, 150, shopMenuButtonImage, "Bomb : 3 coins", 50, "black")
    shopMenu.addButton(4, 50, (HEIGHT // 3) * 2 + 100, 400, 150, shopMenuButtonImage, "EXIT", 50, "black")

    reset = True
    run = True
    pygame.mixer.Sound.play(mainMusic, -1)
    game = Game(screen, bestScore, coins, bombs, pieceSound, launchBombSound, carCollideSound)

    while run:      # mise en place de la boucle principal

        # creer une nouvelle instance du jeu a chaque fois que la fenetre repasse au "game"
        if reset and window == "game":
            game = Game(screen, bestScore, coins, bombs, pieceSound, launchBombSound, carCollideSound)
            reset = False

        # lancement du jeu
        if window == "game":
            screen.fill((128, 129, 129))
            game.update()
            # si le jeux est fermer
            # conservation des variables a sauvegarder et mise a jour du meilleur score du le menu principal
            if game.close:
                bestScore, coins, bombs = game.bestScore, game.coins, game.numberBombs
                window = "menu"
                reset = True
                mainMenu.updateLabel(WIDTH//2 - 175, (HEIGHT //6)*1.5, f"Best Score: {bestScore}", 70, "Blue", 1)

        elif window == "menu":
            mainMenu.update()

        elif window == "shop":
            shopMenu.update()

        # gestion des input de l'utilisateur
        for event in pygame.event.get():
            # si l'event est l'appuie sur la croix de fermeture du jeu
            # fermer le jeu et sauvegarder
            if event.type == pygame.QUIT:
                run = False
                save(bestScore, coins, bombs)

            # quand une touche est enfoncee envoyer l'info dans game
            if event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True

            # quand une touche est relachee envoyer l'info dans game
            if event.type == pygame.KEYUP:
                game.pressed[event.key] = False

            # verifier si le click gauche de la souris est active
            if pygame.mouse.get_pressed(3)[0] and not mouseClick:
                mouseClick = True

                # si on est dans le menu
                # verifier les collision avec tout les boutons du menu principal
                if window == "menu":
                    collide = mainMenu.collide(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

                    # si y a collision activer le son
                    if collide[0]:
                        pygame.mixer.Sound.play(buttonSound)

                        # appuie sur le bouton play
                        if collide[1] == 0:
                            window = "game"

                        # appuie sur le bouton shop
                        # ouvrir le shop et mettre a jour les informations
                        elif collide[1] == 1:
                            window = "shop"
                            shopMenu.updateLabel(80, HEIGHT // 3 - 40, f"coins : {coins}", 50, "black", 3)
                            shopMenu.updateLabel(80, HEIGHT // 3 + 20, f"bombs : {bombs}", 50, "black", 4)

                        # appuie sur le bouton exit
                        # fermeture du jeu et sauvegarde des donnees
                        elif collide[1] == 2:
                            run = False
                            save(bestScore, coins, bombs)

                # si on est dans le shop
                # verifier les collision avec tout les boutons du menu shop
                elif window == "shop":
                    collide = shopMenu.collide(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

                    # appuie sur le bouton pour acheter des bombes
                    # verifier si le joueur a assez de piece puis enlever les piece et ajouter une bombe
                    # mise a jour des information
                    if collide[1] == 3:
                        pygame.mixer.Sound.play(buttonSound)
                        if coins >= 3:
                            bombs += 1
                            coins -= 3
                            shopMenu.updateLabel(80, HEIGHT // 3 - 40, f"coins : {coins}", 50, "black", 3)
                            shopMenu.updateLabel(80, HEIGHT // 3 + 20, f"bombs : {bombs}", 50, "black", 4)

                    # appuie sur le bouton exit
                    # retour au menu principal
                    elif collide[1] == 4:
                        pygame.mixer.Sound.play(buttonSound)
                        window = "menu"

            elif not pygame.mouse.get_pressed(3)[0]:
                mouseClick = False

        pygame.display.flip()
        timer.tick(fps)

def getSave():
    """
    recuperer tout les donnees qui sont stoquer dans le fichier save.txt en les recuperant lignes par lignes
    """
    with open("../save.txt") as file:
        valeursSave = file.readlines()
        bestScore = valeursSave[0]
        coins = valeursSave[1]
        bombs = valeursSave[2]
        file.close()
        return int(bestScore), int(coins), int(bombs)

def save(bestScore, coins, bombs):
    """
    sauvegarde des donnees du jeu pour les recuperer au prochain lancement du jeu
    reecriture des nouvelles donnees par dessus les anciennes donnees
    """
    with open("../save.txt", "w") as file:
        file.write(f"{bestScore}\n")
        file.write(f"{coins}\n")
        file.write(str(bombs))
        file.close()

def clock(screen, time):
    """
    dessin d'une jauge qui se remplie pour verifier si le temps du jeu s'ecoule normalement
    """
    pygame.draw.rect(screen, "green", pygame.Rect(10, 10, 30, 80))
    pygame.draw.rect(screen, "gray", pygame.Rect(10, 10, 30, -(time//100)%80))

if __name__ == '__main__':
    main()