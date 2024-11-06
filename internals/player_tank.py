"""
Player Tank
"""

from typing import TYPE_CHECKING, List, Union

import pygame

from .effects import SHOOTING_SFX
from .bullet import Bullet
from .game_configs import GAME, PLAYER_TANK, TANK_DIRECTION, BULLET

if TYPE_CHECKING:
    from .bot_tank import MovableBotTank


class PlayerTank:
    """Tank object."""

    def __init__(
        self,
        x: float,
        y: float,
        bullet: type[Bullet] = Bullet,
        reload_time: int = 500,
        asset: str = PLAYER_TANK["asset"],
        death_asset: str = PLAYER_TANK["asset"],
        health: int = 6,
        bullet_asset: str = BULLET["asset"],
    ) -> None:
        self.x = x
        self.y = y
        self.speed = 2
        self.direction = "UP"
        self.initial_direction = None
        self.health = health
        self.is_alive = True

        self.asset = asset
        self.death_asset = death_asset
        self.img = pygame.image.load(self.asset)
        self.img = pygame.transform.scale(self.img, PLAYER_TANK["size"])
        self.rect = self.img.get_rect(topleft=(self.x, self.y))

        self.bullet_asset = bullet_asset
        self.bullet = bullet
        self.bullets: List["Bullet"] = []
        self.last_shot_time = 0
        self.bullet_speed = 6
        self.cooldown = reload_time

    def is_colliding_tank(
        self,
        new_rect: pygame.Rect,
        tanks_list: List[Union["PlayerTank", "MovableBotTank"]]
    ) -> bool:
        """Check if tank's position will collide with other tanks."""
        for tank in tanks_list:
            if tank != self and self.is_alive and new_rect.colliderect(tank.rect):
                return True
        return False

    def move_on_keypress(
        self,
        keys: pygame.key.ScancodeWrapper,
        tanks_list: List[Union["PlayerTank", "MovableBotTank"]]
    ) -> None:
        """Movement handler for keys input, check tanks collisions."""
        if not self.is_alive:
            return

        # initial movement variables
        move_x, move_y = 0, 0

        # Only one direction will be chosen based on priority order (LEFT > RIGHT > UP > DOWN)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x = -self.speed
            self.direction = "LEFT"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x = self.speed
            self.direction = "RIGHT"
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y = -self.speed
            self.direction = "UP"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y = self.speed
            self.direction = "DOWN"

        new_x_pos = self.x + move_x
        new_y_pos = self.y + move_y

        new_rect = self.rect.copy()
        new_rect.x = int(new_x_pos)
        new_rect.y = int(new_y_pos)

        if not self.is_colliding_tank(new_rect, tanks_list):
            # restrict movement to screen boundaries
            screen_width, screen_height = GAME["screen_size"]

            # check horizontal boundaries
            if 0 <= new_x_pos <= screen_width - self.rect.width:
                self.x = new_x_pos

            # check vertical boundaries
            if 0 <= new_y_pos <= screen_height - self.rect.height:
                self.y = new_y_pos

            # Update the tank's rectangle to match its new position
            self.rect.topleft = (int(self.x), int(self.y))

    def can_shoot(self) -> bool:
        """Restrict bullets from shooting continuously by setting bullet reload cooldown."""
        if not self.is_alive:
            return False
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.cooldown:
            return True
        return False

    def shoot(self) -> None:
        """Shoot the bullet"""
        if self.can_shoot():
            SHOOTING_SFX.play()

            bullet_center_x = self.x
            bullet_center_y = self.y
            x_shift = 17  # (half_of_tank - half_of_bullet) = (21 - 4)
            y_shift = 13  # (half_of_tank - half_of_bullet) = (23 - 10)

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

            bullet = self.bullet(
                bullet_center_x, bullet_center_y, self.direction, asset=self.bullet_asset)
            self.bullets.append(bullet)
            self.last_shot_time = pygame.time.get_ticks()

    def update_bullets(self) -> None:
        """Remove bullets that're out of screen"""
        self.bullets = [bullet for bullet in self.bullets if bullet.y > 0]

    def process_bullet_collision(
        self,
        tanks_list: List[Union["PlayerTank", "MovableBotTank"]]
    ) -> None:
        """Check if the bullets hit any other tanks and calculate the health on hit."""
        for bullet in self.bullets[:]:
            bullet_rect = pygame.Rect(
                bullet.x, bullet.y, bullet.img.get_width(), bullet.img.get_height())

            for tank in tanks_list:
                if tank == self:
                    continue

                tank_rect = pygame.Rect(
                    tank.x, tank.y, tank.rect.width, tank.rect.height)

                if bullet_rect.colliderect(tank_rect):
                    self.bullets.remove(bullet)
                    tank.health -= 1
                    if tank.health <= 0:
                        tanks_list.remove(tank)
                        tank.is_alive = False
                    break

    def draw(self, screen: pygame.Surface) -> None:
        """Paint the Tank and Bullets"""
        # draw the tank according to direction
        rotated_img = pygame.transform.rotate(
            self.img, TANK_DIRECTION[self.direction])
        center = (self.x + self.rect.width / 2, self.y + self.rect.height / 2)
        rotated_rect = rotated_img.get_rect(center=center)
        screen.blit(rotated_img, rotated_rect.topleft)

        if self.is_alive:
            # draw bullets
            self.update_bullets()
            for bullet in self.bullets:
                bullet.move()
                bullet.draw(screen)
