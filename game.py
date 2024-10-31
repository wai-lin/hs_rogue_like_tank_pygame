"""
Tank game
"""

import math
from os import curdir
import random
from typing import List
import pygame


# game config
GAME = {
    "screen_size": (64 * 15, 64 * 10),
    "background": (0, 0, 0),
}

BULLET = {
    "asset": "assets/imgs/tanks/bullet_dark.png",
    "size": (8, 20)
}

BULLET_DIRECTION = {
    "UP": 0,
    "LEFT": 90,
    "DOWN": 180,
    "RIGHT": 270,
}

TANK = {
    "asset": "assets/imgs/tanks/tank_dark.png",
    "death_asset": "assets/imgs/tanks/tank_dark_body.png",
    "size": (42, 46),
}

TANK_DIRECTION = {
    "DOWN": 0,
    "RIGHT": 90,
    "UP": 180,
    "LEFT": 270,
}

TILES = {
    # grass tiles
    "grass_1": "tile_grass_1.png",
    "grass_2": "tile_grass_2.png",
    "grass_road_CornerLL": "tile_grass_road_CornerLL.png",
    "grass_road_CornerLR": "tile_grass_road_CornerLR.png",
    "grass_road_CornerUL": "tile_grass_road_CornerUL.png",
    "grass_road_CornerUR": "tile_grass_road_CornerUR.png",
    "grass_road_Crossing": "tile_grass_road_Crossing.png",
    "grass_road_CrossingRound": "tile_grass_road_CrossingRound.png",
    "grass_road_East": "tile_grass_road_East.png",
    "grass_road_North": "tile_grass_road_North.png",
    "grass_road_SplitE": "tile_grass_road_SplitE.png",
    "grass_road_SplitN": "tile_grass_road_SplitN.png",
    "grass_road_SplitS": "tile_grass_road_SplitS.png",
    "grass_road_SplitW": "tile_grass_road_SplitW.png",

    # transitional tiles
    "grass_road_TransitionE": "tile_grass_road_TransitionE.png",
    "grass_road_TransitionE_dirt": "tile_grass_road_TransitionE_dirt.png",
    "grass_road_TransitionN": "tile_grass_road_TransitionN.png",
    "grass_road_TransitionN_dirt": "tile_grass_road_TransitionN_dirt.png",
    "grass_road_TransitionS": "tile_grass_road_TransitionS.png",
    "grass_road_TransitionS_dirt": "tile_grass_road_TransitionS_dirt.png",
    "grass_road_TransitionW": "tile_grass_road_TransitionW.png",
    "grass_road_TransitionW_dirt": "tile_grass_road_TransitionW_dirt.png",
    "grass_transitionE": "tile_grass_transitionE.png",
    "grass_transitionN": "tile_grass_transitionN.png",
    "grass_transitionS": "tile_grass_transitionS.png",
    "grass_transitionW": "tile_grass_transitionW.png",

    # sand tiles
    "sand_1": "tile_sand_1.png",
    "sand_2": "tile_sand_2.png",
    "sand_road_CornerLL": "tile_sand_road_CornerLL.png",
    "sand_road_CornerLR": "tile_sand_road_CornerLR.png",
    "sand_road_CornerUL": "tile_sand_road_CornerUL.png",
    "sand_road_CornerUR": "tile_sand_road_CornerUR.png",
    "sand_road_Crossing": "tile_sand_road_Crossing.png",
    "sand_road_CrossingRound": "tile_sand_road_CrossingRound.png",
    "sand_road_East": "tile_sand_road_East.png",
    "sand_road_North": "tile_sand_road_North.png",
    "sand_road_SplitE": "tile_sand_road_SplitE.png",
    "sand_road_SplitN": "tile_sand_road_SplitN.png",
    "sand_road_SplitS": "tile_sand_road_SplitS.png",
    "sand_road_SplitW": "tile_sand_road_SplitW.png",
}

TILE = {
    "asset": "assets/imgs/tiles/tile_grass_1.png",
    "size": (64, 64),
}

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
    """Drawing map on screen."""
    for row, _ in enumerate(MAP):
        for col, _ in enumerate(MAP[row]):
            tile_type = MAP[row][col]
            tile_asset = TILES[tile_type]
            img = pygame.image.load(f"assets/imgs/tiles/{tile_asset}")
            img = pygame.transform.scale(img, TILE["size"])
            pos_x = col * TILE["size"][0]
            pos_y = row * TILE["size"][1]
            screen.blit(img, (pos_x, pos_y))


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


class Tank:
    """Tank object."""

    def __init__(
        self,
        x: float,
        y: float,
        bullet: type[Bullet] = Bullet,
        reload_time: int = 500,
        asset: str = TANK["asset"],
        death_asset: str = TANK["asset"],
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
        self.img = pygame.transform.scale(self.img, TANK["size"])
        self.rect = self.img.get_rect(topleft=(self.x, self.y))

        self.bullet_asset = bullet_asset
        self.bullet = bullet
        self.bullets: List["Bullet"] = []
        self.last_shot_time = 0
        self.bullet_speed = 6
        self.cooldown = reload_time

    def check_tank_collision(self, new_rect: pygame.Rect, tanks_list: List["Tank"]) -> bool:
        """Check if tank's position will collide with other tanks."""
        for tank in tanks_list:
            if tank != self and self.is_alive and new_rect.colliderect(tank.rect):
                return True
        return False

    def move_on_keypress(self, keys: pygame.key.ScancodeWrapper, tanks_list: List["Tank"]) -> None:
        """Movement handler for keys input, check tanks collisions."""
        if not self.is_alive:
            return

        # initial movement variables
        move_x, move_y = 0, 0

        if self.initial_direction is None:
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

        new_x_pos = self.x + move_x
        new_y_pos = self.y + move_y

        new_rect = self.rect.copy()
        new_rect.x = int(new_x_pos)
        new_rect.y = int(new_y_pos)

        if not self.check_tank_collision(new_rect, tanks_list):
            # restrict movement to screen boundries
            screen_width, screen_height = GAME["screen_size"]

            # check horizonal boundries
            if 0 <= new_x_pos <= screen_width - self.rect.width:
                self.x = new_x_pos

            # check vertical boundries
            if 0 <= new_y_pos <= screen_height - self.rect.height:
                self.y += move_y

            # Update the tank's rectangle to match its new position
            self.rect.topleft = (int(self.x), int(self.y))

        # reset starting direction if no key pressed
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.initial_direction = None

    def move(self, direction: str) -> None:
        """Move tank according to key press direction."""
        if self.health <= 0:
            return
        self.direction = direction
        rad_angle = math.radians(TANK_DIRECTION[direction])
        self.x += self.speed * math.sin(rad_angle)
        self.y += self.speed * math.cos(rad_angle)

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

    def check_bullet_collision(self, tanks_list: List["Tank"]) -> None:
        """Check if the bullets hit any other tanks."""
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
                        tank.is_alive = False
                        tank.img = pygame.image.load(tank.death_asset)
                        tank.img = pygame.transform.scale(
                            tank.img, TANK["size"])
                        tank.img = pygame.transform.rotate(
                            tank.img, TANK_DIRECTION[tank.direction])
                    break

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
        """Paint the Tank and Bullets"""
        # draw the tank according to direction
        rotated_img = pygame.transform.rotate(
            self.img, TANK_DIRECTION[self.direction])
        center = (self.x + self.rect.width / 2, self.y + self.rect.height / 2)
        rotated_rect = rotated_img.get_rect(center=center)
        screen.blit(rotated_img, rotated_rect.topleft)

        if self.is_alive:
            # display health bar above tank
            self.draw_health_bar(screen)

            # draw bullets
            self.update_bullets()
            for bullet in self.bullets:
                bullet.move()
                bullet.draw(screen)

class BotTank(Tank):
    """BotTank object."""

    def __init__(
                self,
                x: float,
                y: float,
                bullet: type[Bullet] = Bullet,
                reload_time: int = 500,
                asset: str = TANK["asset"],
                death_asset: str = TANK["asset"],
                health: int = 6,
                bullet_asset: str = BULLET["asset"],
                movement_interval: int = 2_000
            ) -> None:
        super().__init__(
                x,
                y,
                bullet,
                asset=asset,
                reload_time=reload_time,
                death_asset=death_asset,
                health=health,
                bullet_asset=bullet_asset
            )
        self.movement_interval = movement_interval
        self.last_move_time = pygame.time.get_ticks()
        self.current_direction = self.get_new_direction()

    def get_new_direction(self) -> str:
        """Get random direction"""
        return random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

    def update_movement(self):
        """Change new tank movement, according to movement interval."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.movement_interval:
            self.current_direction = self.get_new_direction()
            self.last_move_time = current_time
        self.move(self.current_direction)


# setup the game
pygame.init()
screen = pygame.display.set_mode(GAME["screen_size"])
clock = pygame.time.Clock()

# objects
player = Tank(
    x=300,
    y=200,
    asset="assets/imgs/tanks/tank_green.png",
    death_asset="assets/imgs/tanks/tank_green_body.png",
    bullet_asset="assets/imgs/tanks/bullet_green.png",
)
bot_1 = BotTank(
    x=100,
    y=50,
    asset="assets/imgs/tanks/tank_red.png",
    death_asset="assets/imgs/tanks/tank_red_body.png",
    bullet_asset="assets/imgs/tanks/bullet_red.png",
    movement_interval=2_000,
)
bot_2 = BotTank(
    x=200,
    y=50,
    asset="assets/imgs/tanks/tank_blue.png",
    death_asset="assets/imgs/tanks/tank_blue_body.png",
    bullet_asset="assets/imgs/tanks/bullet_blue.png",
    movement_interval=3_000,
)
bot_3 = BotTank(
    x=300,
    y=50,
    asset="assets/imgs/tanks/tank_sand.png",
    death_asset="assets/imgs/tanks/tank_sand_body.png",
    bullet_asset="assets/imgs/tanks/bullet_sand.png",
    movement_interval=2_500,
)

all_tanks = [bot_1, bot_2, bot_3, player]


def sort_alive_tanks_on_last(t: "Tank"):
    return t.is_alive


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
    player.move_on_keypress(keys, all_tanks)
    if keys[pygame.K_SPACE]:
        player.shoot()
    player.check_bullet_collision(all_tanks)

    """
    Screen painting
    """
    # fill background color
    screen.fill(GAME["background"])
    # draw map
    draw_map(screen)

    # draw the tank and bullets
    # show the alive tanks on top of the dead tanks
    all_tanks.sort(key=sort_alive_tanks_on_last)
    for tank in all_tanks:
        if isinstance(tank, BotTank):
            tank.update_movement()
        tank.draw(screen)

    """
    Wrap-Ups
    """
    # update the display
    pygame.display.flip()
    # cap the fps at 60
    clock.tick(60)

# exit game
pygame.quit()
