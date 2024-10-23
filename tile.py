"""
Tile object
"""
import pygame

TILE = {
    "asset": "assets/PNG/Retina/tileSand1.png",
    "size": (64, 64),
}

class Tile:
    def __init__(self, asset=TILE["asset"]) -> None:
        self.img = pygame.image.load(asset)
        self.img = pygame.transform.scale(self.img, TILE["size"])

    def draw_tiles(self, screen: pygame.Surface, rows: int, cols: int) -> None:
        x_tile_size = TILE["size"][0]
        y_tile_size = TILE["size"][1]
        for row in range(rows):
            for col in range(cols):
                x = col * x_tile_size
                y = row * y_tile_size
                screen.blit(self.img, (x, y))

    # def draw_tile_map(self, screen: pygame.Surface, tile_map: list[list[int]]):
    #     x_tile_size = TILE["size"][0]
    #     y_tile_size = TILE["size"][1]
    #     for row in range(len(tile_map)):
    #         for col in range(len(tile_map[row])):
    #             tile = tile_map[row][col]
    #             x = col * x_tile_size
    #             y = row * y_tile_size
    #
    #             if tile == 0:
    #                 screen.blit()
    #             elif tile == 1:
