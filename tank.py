"""
Tank object
"""
import pygame
import math

from bullet import Bullet

TANK = {
    "asset": "assets/PNG/Retina/tank_dark.png",
    "size": (42, 46),
}

DIRECTION = {
    "DOWN": 0,
    "RIGHT": 90,
    "UP": 180,
    "LEFT": 270,
}

class Tank:
    """Tank object factory."""
    def __init__(self, x: float, y: float, bullet=Bullet, reload_time=1000, asset=TANK["asset"]) -> None:
        self.x = x
        self.y = y
        self.speed = 2
        self.direction = "UP"
        self.initial_direction = None

        self.img = pygame.image.load(asset)
        self.img = pygame.transform.scale(self.img, TANK["size"])
        self.rect = self.img.get_rect(center=(400, 300))

        self.bullet = bullet
        self.bullets = []
        self.last_shot_time = 0
        self.bullet_speed = 6
        self.cooldown = reload_time

    def move_on_keypress(self, keys: pygame.key.ScancodeWrapper) -> None:
        # initial movement variables
        move_x, move_y = 0, 0

        if self.initial_direction == None:
            if keys[pygame.K_LEFT]:
                self.initial_direction = "LEFT"
            if keys[pygame.K_RIGHT]:
                self.initial_direction = "RIGHT"
            if keys[pygame.K_UP]:
                self.initial_direction = "UP"
            if keys[pygame.K_DOWN]:
                self.initial_direction = "DOWN"

        # horizontal movements
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            move_x = -self.speed
            if self.initial_direction == "LEFT":
                self.direction = "LEFT"
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            move_x = self.speed
            if self.initial_direction == "RIGHT":
                self.direction = "RIGHT"

        # vertical movements
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            move_y = -self.speed
            if self.initial_direction == "UP":
                self.direction = "UP"
        if keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            move_y = self.speed
            if self.initial_direction == "DOWN":
                self.direction = "DOWN"

        # normalize movements
        if move_x != 0 and move_y != 0:
            move_x /= math.sqrt(2)
            move_y /= math.sqrt(2)

        # reset starting direction if no key pressed
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.initial_direction = None

        # move tank position
        self.x += move_x
        self.y += move_y

    def move(self, direction: str) -> None:
        """Move tank according to key press direction."""
        self.direction = direction
        rad_angle = math.radians(DIRECTION[direction])
        self.x += self.speed * math.sin(rad_angle)
        self.y += self.speed * math.cos(rad_angle)

    def can_shoot(self) -> bool:
        """Restrict bullets from shooting continuously by setting bullet reload cooldown."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.cooldown:
            return True
        return False

    def shoot(self) -> None:
        """Shoot the bullet"""
        if self.can_shoot():
            bullet_center_x = self.x
            bullet_center_y = self.y
            x_shift = 17 # (half_of_tank - half_of_bullet) = (21 - 4)
            y_shift = 13 # (half_of_tank - half_of_bullet) = (23 - 10)

            if self.direction == "UP":
                bullet_center_x = self.x + x_shift
                bullet_center_y = self.y - y_shift
            if self.direction == "DOWN":
                bullet_center_x = self.x + x_shift
                bullet_center_y = self.y + (3 * y_shift)
            if self.direction == "LEFT":
                bullet_center_x = self.x - x_shift
                bullet_center_y = self.y + (1.4 * y_shift)
            if self.direction == "RIGHT":
                bullet_center_x = self.x + (3 * x_shift)
                bullet_center_y = self.y + (1.4 * y_shift)

            bullet = self.bullet(bullet_center_x, bullet_center_y, self.direction)
            self.bullets.append(bullet)
            self.last_shot_time = pygame.time.get_ticks()

    def update_bullets(self) -> None:
        """Remove bullets that're out of screen"""
        self.bullets = [bullet for bullet in self.bullets if bullet.y > 0]

    def draw(self, screen: pygame.Surface) -> None:
        """Paint the Tank and Bullets"""
        # rotate_direction = self.initial_direction or "UP"
        rotated_img = pygame.transform.rotate(self.img, DIRECTION[self.direction])
        # screen.blit(rotated_img, (self.x, self.y))
        center = (self.x + self.rect.width / 2, self.y + self.rect.height / 2)
        rotated_rect = rotated_img.get_rect(center=center)
        screen.blit(rotated_img, rotated_rect.topleft)

        # draw bullets
        self.update_bullets()
        for bullet in self.bullets:
            bullet.move()
            bullet.draw(screen)

