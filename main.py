"""
Tank Shooter Game
"""

import pygame

from tank import Tank
from tile import Tile

# game config
GAME = {
    "screen_size": (800, 640),
    "background": (0, 0, 0),
}

# setup the game
pygame.init()
screen = pygame.display.set_mode(GAME["screen_size"])
clock = pygame.time.Clock()

# objects
tile = Tile()
player = Tank(300, 400)

# game loop
RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    # handle keypress
    keys = pygame.key.get_pressed()

    # move on arrows
    if keys[pygame.K_LEFT]:
        player.move("LEFT")
    if keys[pygame.K_RIGHT]:
        player.move("RIGHT")
    if keys[pygame.K_UP]:
        player.move("UP")
    if keys[pygame.K_DOWN]:
        player.move("DOWN")

    # shoot on spacebar
    if keys[pygame.K_SPACE]:
        player.shoot()

    # fill background color
    screen.fill(GAME["background"])

    # draw tiles
    tile.draw_tiles(screen, 20, 25)

    # draw the tank and bullets
    player.draw(screen)

    # update the display
    pygame.display.flip()

    # cap the fps at 60
    clock.tick(60)

# exit game
pygame.quit()

