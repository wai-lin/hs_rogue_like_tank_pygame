"""
Generate game map
"""

import pygame

from .game_configs import TILE, TILES

MAP = [
    ["grass_1", "grass_2", "grass_road_SplitE", "grass_road_East", "grass_road_East", "grass_road_East", "grass_road_TransitionE",
        "sand_road_CornerLL", "sand_1", "sand_2", "sand_1", "sand_2", "sand_road_North", "sand_2", "sand_1"],
    ["grass_1", "grass_2", "grass_road_North", "grass_2", "grass_1", "grass_2", "grass_transitionE", "sand_road_CornerUR",
        "sand_road_CornerLL", "sand_2", "sand_1", "sand_2", "sand_road_SplitE", "sand_road_East", "sand_road_East"],
    ["grass_1", "grass_2", "grass_road_North", "grass_2", "grass_1", "grass_2", "grass_transitionE",
        "sand_2", "sand_road_North", "sand_2", "sand_1", "sand_2", "sand_road_North", "sand_2", "sand_1"],
    ["grass_1", "grass_2", "grass_road_North", "grass_2", "grass_1", "grass_2", "grass_transitionE",
        "sand_2", "sand_road_North", "sand_2", "sand_1", "sand_2", "sand_road_North", "sand_2", "sand_1"],
    ["grass_road_East", "grass_road_East", "grass_road_Crossing", "grass_road_East", "grass_road_CornerLL", "grass_2",
        "grass_transitionE", "sand_2", "sand_road_North", "sand_2", "sand_1", "sand_2", "sand_road_North", "sand_2", "sand_1"],
    ["grass_1", "grass_2", "grass_road_North", "grass_2", "grass_road_North", "grass_2", "grass_transitionE", "sand_2",
        "sand_road_CornerUR", "sand_road_East", "sand_road_East", "sand_road_East", "sand_road_CornerUL", "sand_2", "sand_1"],
    ["grass_1", "grass_2", "grass_road_North", "grass_2", "grass_road_North", "grass_2",
        "grass_transitionE", "sand_2", "sand_1", "sand_2", "sand_1", "sand_2", "sand_1", "sand_2", "sand_1"],
    ["grass_1", "grass_2", "grass_road_North", "grass_2", "grass_road_North", "grass_2", "grass_transitionE", "sand_2",
        "sand_1", "sand_2", "sand_road_CornerLR", "sand_road_East", "sand_road_East", "sand_road_East", "sand_road_East"],
    ["grass_1", "grass_2", "grass_road_CornerUR", "grass_road_East", "grass_road_SplitN", "grass_road_East", "grass_road_TransitionE",
        "sand_road_East", "sand_road_East", "sand_road_East", "sand_road_CornerUL", "sand_2", "sand_1", "sand_2", "sand_1"],
    ["grass_1", "grass_2", "grass_1", "grass_2", "grass_1", "grass_2", "grass_transitionE",
        "sand_2", "sand_1", "sand_2", "sand_1", "sand_2", "sand_1", "sand_2", "sand_1"],
]


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
