"""
Tank Shooter Game
"""

import pygame

from tank import Tank
from tile import Tile

# game config
GAME = {
    "screen_size": (64 * 15, 64 * 10),
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

    """
    Player actions
    """
    player.move_on_keypress(keys)
    if keys[pygame.K_SPACE]:
        player.shoot()

    """
    Map painting
    """
    # fill background color
    screen.fill(GAME["background"])
    # draw tiles
    tile.draw_tiles(screen, 20, 25)
    # draw the tank and bullets
    player.draw(screen)

    """
    Wrap-Ups
    """
    # update the display
    pygame.display.flip()
    # cap the fps at 60
    clock.tick(60)

# exit game
pygame.quit()

