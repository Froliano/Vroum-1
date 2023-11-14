import pygame
from game import Game
from player import Player
from init import WIDTH, HEIGHT

pygame.init()

WIDTH, HEIGHT = (500, 800)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    timer = pygame.time.Clock()
    fps = 60

    game = Game(screen)
    run = True

    while run:      # mise en place de la boucle principale
        screen.fill((128, 129, 129))

        game.update()
        clock(screen, pygame.time.get_ticks())

        for event in pygame.event.get():        # gestion des input de l'utilisateur
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True
            if event.type == pygame.KEYUP:
                game.pressed[event.key] = False

        pygame.display.flip()
        timer.tick(fps)

def clock(screen, time):
    pygame.draw.rect(screen, "green", pygame.Rect(10, 10, 30, 80))
    pygame.draw.rect(screen, "gray", pygame.Rect(10, 10, 30, -(time//100)%80))

if __name__ == '__main__':
    main()