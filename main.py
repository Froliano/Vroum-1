import sys
import time

import pygame_menu
import pygame

from game import Game
from menu import Menu
from init import WIDTH, HEIGHT

pygame.init()

def main():

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    timer = pygame.time.Clock()
    fps = 60
    window = "menu"

    bestScore, coins, bombs = getSave()

    bgMainMenu = pygame.image.load("bgMenu.png")
    bgMainMenu = pygame.transform.scale(bgMainMenu, (WIDTH, HEIGHT))
    mainMenuButtonImage = pygame.image.load("greenButton.png")

    mainMenu = Menu(screen, bgMainMenu)
    mainMenu.addLabel(WIDTH//2 - 150, HEIGHT //12, "VROUM 1", 100, "blue")
    mainMenu.addLabel(WIDTH//2 - 175, (HEIGHT //6)*1.5, f"Best Score: {bestScore}", 70, "Blue")
    mainMenu.addButton(0, WIDTH//2 - 100, (HEIGHT //3)*1.5, 200, 70, mainMenuButtonImage, "PLAY", 50, "Blue")
    mainMenu.addButton(1, WIDTH//2 - 100, (HEIGHT //3)*2, 200, 70, mainMenuButtonImage, "SHOP", 50, "Blue")
    mainMenu.addButton(2, WIDTH//2 - 100, (HEIGHT //3)*2.5, 200, 70, mainMenuButtonImage, "EXIT", 50, "Blue")

    bgShopMenu = pygame.image.load("shopBG.png")
    bgShopMenu = pygame.transform.scale(bgShopMenu, (WIDTH, HEIGHT))
    shopMenuButtonImage = pygame.image.load("redButton.png")

    shopMenu = Menu(screen, bgShopMenu)
    shopMenu.addLabel(WIDTH//2 - 80, HEIGHT //12, "SHOP", 100, "white")
    shopMenu.addButton(3,50, (HEIGHT // 3) , 400, 150, shopMenuButtonImage, "Bomb : 3 coins", 50, "black")
    shopMenu.addButton(4, 50, (HEIGHT // 3) * 2, 400, 150, shopMenuButtonImage, "EXIT", 50, "black")

    reset = True
    run = True

    while run:      # mise en place de la boucle principale
        if reset and window == "game":
            game = Game(screen, bestScore, coins, bombs)
            reset = False
        if window == "game":
            screen.fill((128, 129, 129))
            game.update()
            if game.close:
                bestScore, coins, bombs = game.bestScore, game.coins, game.numberBombs
                window = "menu"
                reset = True

        elif window == "menu":
            mainMenu.update()
        elif window == "shop":
            shopMenu.update()

        for event in pygame.event.get():        # gestion des input de l'utilisateur
            if event.type == pygame.QUIT:
                run = False
                save(bestScore, coins, bombs)
            if event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True
            if event.type == pygame.KEYUP:
                game.pressed[event.key] = False
            if pygame.mouse.get_pressed(3)[0]:
                if window == "menu":
                    collide = mainMenu.collide(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    if collide[0]:
                        if collide[1] == 0:
                            window = "game"
                        elif collide[1] == 1:
                            window = "shop"
                        elif collide[1] == 2:
                            run = False
                            save(bestScore, coins, bombs)
                elif window == "shop":
                    collide = shopMenu.collide(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    if collide[1] == 3:
                        if coins >= 3:
                            bombs += 1
                            coins -= 3
                            print(coins, bombs)
                    elif collide[1] == 4:
                        window = "menu"

        pygame.display.flip()
        timer.tick(fps)

def getSave():
    with open("save.txt") as file:
        valeursSave = file.readlines()
        bestScore = valeursSave[0][0:len(valeursSave)-2]
        coins = valeursSave[1][0:len(valeursSave)-2]
        bombs = valeursSave[2]
        file.close()
        return int(bestScore), int(coins), int(bombs)

def save(bestScore, coins, bombs):
    with open("save.txt", "w") as file:
        file.write(f"{bestScore}\n")
        file.write(f"{coins}\n")
        file.write(str(bombs))
        file.close()

def clock(screen, time):
    pygame.draw.rect(screen, "green", pygame.Rect(10, 10, 30, 80))
    pygame.draw.rect(screen, "gray", pygame.Rect(10, 10, 30, -(time//100)%80))

if __name__ == '__main__':
    main()