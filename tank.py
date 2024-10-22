"""
Tank object
"""
import pygame

from bullet import Bullet

TANK = {
    "asset": "assets/PNG/Retina/tank_dark.png",
    "size": (32, 32),
}

DIRECTION = {
    "DOWN": 0,
    "RIGHT": 90,
    "UP": 180,
    "LEFT": 270,
}

class Tank:
    def __init__(self, x, y, bullet=Bullet, reload_time=1000, asset=TANK["asset"]) -> None:
        self.x = x
        self.y = y
        self.speed = 5

        self.img = pygame.image.load(asset)
        self.img = pygame.transform.scale(self.img, TANK["size"])
        self.rect = self.img.get_rect(center=(400, 300))
        self.direction = "UP"

        self.Bullet = bullet
        self.bullets = []
        self.last_shot_time = 0
        self.bullet_speed = 6
        self.cooldown = reload_time

    def move(self, direction: str) -> None:
        self.direction = direction
        if direction == "UP":
            self.direction = "UP"
            self.y -= self.speed
        elif direction == "RIGHT":
            self.direction = "RIGHT"
            self.x += self.speed
        elif direction == "DOWN":
            self.direction = "DOWN"
            self.y += self.speed
        elif direction == "LEFT":
            self.direction = "LEFT"
            self.x -= self.speed

    def can_shoot(self) -> bool:
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.cooldown:
            return True
        return False

    def shoot(self) -> None:
        if self.can_shoot():
            bullet_center_x = self.x
            bullet_center_y = self.y

            if self.direction == "UP" or self.direction == "DOWN":
                bullet_center_x = self.x + 11 # (16 - 5)
            if self.direction == "RIGHT" or self.direction == "LEFT":
                bullet_center_y = self.y + 11 # (16 - 5)

            bullet = self.Bullet(bullet_center_x, bullet_center_y, self.direction)
            self.bullets.append(bullet)
            self.last_shot_time = pygame.time.get_ticks()

    def update_bullets(self) -> None:
        self.bullets = [bullet for bullet in self.bullets if bullet.y > 0]

    def draw(self, screen: pygame.Surface) -> None:
        rotated_img = pygame.transform.rotate(self.img, DIRECTION[self.direction])
        # rotated_rect = rotated_img.get_rect(center=self.rect.center)
        screen.blit(rotated_img, (self.x, self.y))
        self.update_bullets()
        for bullet in self.bullets:
            bullet.move()
            bullet.draw(screen)

