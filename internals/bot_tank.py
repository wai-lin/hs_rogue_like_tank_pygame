"""
Bot Tanks
"""

from typing import TYPE_CHECKING, List, Union, Tuple

import math
import random
import pygame

from .game_configs import GAME, BOT_TANK, TANK_DIRECTION

if TYPE_CHECKING:
    from .player_tank import PlayerTank


class BotEnemy:
    """BotEnemy object."""

    def __init__(
        self,
        x: float,
        y: float,
        asset: str = BOT_TANK["asset"],
        death_asset: str = BOT_TANK["asset"],
        health: int = 6,
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
        self.img = pygame.transform.scale(self.img, BOT_TANK["size"])
        self.rect = self.img.get_rect(topleft=(self.x, self.y))

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

    def move(
        self,
        direction: str,
        tanks_list: List[Union["PlayerTank", "MovableBotTank"]]
    ) -> None:
        """Move tank according to direction, with boundary check and collision avoidance."""
        if self.health <= 0:
            return
        self.direction = direction
        rad_angle = math.radians(TANK_DIRECTION[direction])

        # Calculate potential new position based on direction and speed
        new_x = self.x + self.speed * math.sin(rad_angle)
        new_y = self.y + self.speed * math.cos(rad_angle)
        new_rect = self.rect.copy()
        new_rect.topleft = (int(new_x), int(new_y))

        # Ensure the new position is within screen boundaries
        screen_width, screen_height = GAME["screen_size"]
        is_within_screen_width = 0 <= new_x <= screen_width - self.rect.width
        is_within_screen_height = 0 <= new_y <= screen_height - self.rect.height
        if is_within_screen_width and is_within_screen_height:
            # Check if the new position collides with any other tank
            if not self.is_colliding_tank(new_rect, tanks_list):
                self.x, self.y = new_x, new_y
                self.rect.topleft = (int(self.x), int(self.y))

    def draw_health_bar(self, screen: pygame.Surface) -> None:
        """Draw the health bar with six boxes above the tank."""
        bar_width = 8
        bar_height = 8
        spacing = 2
        # center the bar above the tank
        bar_x = self.x - (self.rect.width // 2) + \
            (3 * (bar_width + spacing)) // 2
        bar_y = self.y - 20  # position above the tank

        fill_color = (239, 68, 68)  # red
        outline_color = (15, 23, 42)  # dark blue

        # draw the health boxes
        for i in range(self.health):
            box_rect = (bar_x + i * (bar_width + spacing),
                        bar_y, bar_width, bar_height)
            # health box
            pygame.draw.rect(screen, fill_color, box_rect)
            # health outline box
            pygame.draw.rect(screen, outline_color, box_rect, 2)

    def draw(self, screen: pygame.Surface) -> None:
        """Paint the Tank"""
        # draw the tank according to direction
        rotated_img = pygame.transform.rotate(
            self.img, TANK_DIRECTION[self.direction])
        center = (self.x + self.rect.width / 2, self.y + self.rect.height / 2)
        rotated_rect = rotated_img.get_rect(center=center)
        screen.blit(rotated_img, rotated_rect.topleft)

        if self.is_alive:
            # display health bar above tank
            self.draw_health_bar(screen)


class MovableBotTank(BotEnemy):
    """Movable BotTank object."""

    def __init__(
        self,
        x: float,
        y: float,
        asset: str = BOT_TANK["asset"],
        death_asset: str = BOT_TANK["asset"],
        health: int = 6,
        movement_interval: int = 2_000
    ) -> None:
        super().__init__(
            x,
            y,
            asset=asset,
            death_asset=death_asset,
            health=health,
        )
        self.movement_interval = movement_interval
        self.last_move_time = pygame.time.get_ticks()
        self.current_direction = self.get_new_direction()

    def get_new_direction(self) -> str:
        """Get random direction"""
        return random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

    def move_randomly(self, tanks_list: List[Union["PlayerTank", "MovableBotTank"]]):
        """Change new tank movement, according to movement interval."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.movement_interval:
            self.current_direction = self.get_new_direction()
            self.last_move_time = current_time
        self.move(self.current_direction, tanks_list)


def generate_bots():
    """Try to generate bots that are not overlap with each other."""

    tank_size_w: int = BOT_TANK["size"][0]
    tank_size_h: int = BOT_TANK["size"][1]
    bots_count: int = GAME["bots_count"]

    x_coords = (100, 900)
    y_coords = (100, 500)
    coordinates: List[Tuple[int, int]] = []

    bot_tanks: List[MovableBotTank] = []

    for _ in range(bots_count):
        x = random.randint(x_coords[0], x_coords[1])
        y = random.randint(y_coords[0], y_coords[1])
        new_rect = pygame.Rect(x, y, tank_size_w, tank_size_h)

        attempt = 0
        max_attempts = 50  # limit the number of attempts to find a non-overlapping position
        while attempt < max_attempts:
            is_colliding_with_tanks = any(
                new_rect.colliderect(
                    pygame.Rect(cx, cy, tank_size_w, tank_size_h)
                ) for cx, cy in coordinates
            )

            if not is_colliding_with_tanks:
                coordinates.append((x, y))
                break
            attempt += 1

        if attempt == max_attempts:
            x = random.randint(x_coords[0], x_coords[1])
            y = random.randint(y_coords[0], y_coords[1])
            new_rect = pygame.Rect(x, y, tank_size_w, tank_size_h)

        bot = MovableBotTank(
            x=x,
            y=y,
            health=1,
            asset=BOT_TANK["asset"],
            death_asset=BOT_TANK["death_asset"],
            movement_interval=random.choice(GAME["bot_intervals"]),
        )
        bot_tanks.append(bot)

    return bot_tanks


def has_player_won(bot_tanks: List[MovableBotTank]):
    """Check if player has won the game."""
    return all(not bot.is_alive for bot in bot_tanks)
