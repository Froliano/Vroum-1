import pygame

from game import Game
from init import WIDTH, HEIGHT

pygame.init()

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    timer = pygame.time.Clock()
    fps = 60

    bestScore, coins = getSave()
    game = Game(screen, bestScore, coins)
    window = "game"
    getSave()

    run = True

    while run:      # mise en place de la boucle principale

        if window == "game":
            screen.fill((128, 129, 129))
            game.update()
        elif window == "menu":
            pass
        elif window == "game over":
            pass

        for event in pygame.event.get():        # gestion des input de l'utilisateur
            if event.type == pygame.QUIT:
                run = False
                save(game.bestScore, game.coins)
            if event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True
            if event.type == pygame.KEYUP:
                game.pressed[event.key] = False

        pygame.display.flip()
        timer.tick(fps)

def getSave():
    with open("save.txt") as file:
        valeursSave = file.readlines()
        bestScore = valeursSave[0][0:len(valeursSave)-3]
        coins = valeursSave[1]
        file.close()
        return int(bestScore), int(coins)

def save(bestScore, coins):
    with open("save.txt", "w") as file:
        file.write(f"{bestScore}\n")
        file.write(str(coins))
        file.close()



def clock(screen, time):
    pygame.draw.rect(screen, "green", pygame.Rect(10, 10, 30, 80))
    pygame.draw.rect(screen, "gray", pygame.Rect(10, 10, 30, -(time//100)%80))

if __name__ == '__main__':
    main()