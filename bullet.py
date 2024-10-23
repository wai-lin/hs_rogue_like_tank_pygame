"""
Bullet object
"""

import pygame

BULLET = {
    "asset": "assets/PNG/Retina/bulletDark1.png",
    "size": (8, 20)
}

DIRECTION = {
    "UP": 0,
    "LEFT": 90,
    "DOWN": 180,
    "RIGHT": 270,
}

class Bullet:
    def __init__(self, x: float, y: float, direction: str, asset: str=BULLET["asset"]) -> None:
        self.x = x
        self.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 6

        self.img = pygame.image.load(asset)
        self.img = pygame.transform.scale(self.img, BULLET["size"])
        self.img = pygame.transform.rotate(self.img, DIRECTION[direction])

        if direction == "UP":
            self.speed_y = -6
        if direction == "RIGHT":
            self.speed_x = 6
        if direction == "DOWN":
            self.speed_y = 6
        if direction == "LEFT":
            self.speed_x = -6

    def move(self) -> None:
        self.y += self.speed_y
        self.x += self.speed_x

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.img, (self.x, self.y))

