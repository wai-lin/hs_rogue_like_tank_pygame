"""
Tank Bullet 
"""

import pygame

from .game_configs import BULLET, BULLET_DIRECTION


class Bullet:
    """Bullet object."""

    def __init__(self, x: float, y: float, direction: str,  asset: str = BULLET["asset"]) -> None:
        self.x = x
        self.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 6

        self.img = pygame.image.load(asset)
        self.img = pygame.transform.scale(self.img, BULLET["size"])
        self.img = pygame.transform.rotate(
            self.img, BULLET_DIRECTION[direction])

        if direction == "UP":
            self.speed_y = -6
        if direction == "RIGHT":
            self.speed_x = 6
        if direction == "DOWN":
            self.speed_y = 6
        if direction == "LEFT":
            self.speed_x = -6

    def move(self) -> None:
        """Move bullet to x and y."""
        self.y += self.speed_y
        self.x += self.speed_x

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the bullet according to x and y."""
        screen.blit(self.img, (self.x, self.y))
