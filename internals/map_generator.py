"""
Generate game map
"""

import pygame

from .game_configs import TILE, TILES, MAP


def draw_map(screen: pygame.Surface) -> None:
    """Draw the map on screen."""
    for row, _ in enumerate(MAP):
        for col, _ in enumerate(MAP[row]):
            tile_type = MAP[row][col]
            tile_asset = TILES[tile_type]
            img = pygame.image.load(f"assets/imgs/tiles/{tile_asset}")
            img = pygame.transform.scale(img, TILE["size"])
            pos_x = col * TILE["size"][0]
            pos_y = row * TILE["size"][1]
            screen.blit(img, (pos_x, pos_y))
