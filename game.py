"""
Tank game
"""

import math
import random
import pygame

from enum import Enum
from typing import Tuple, List, Dict, Set

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

class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

class MapTile:
    def __init__(self, tile_type: str) -> None:
        self.tile_type = tile_type
        self.img: None | pygame.Surface = None
        self.roads: Set[Direction] = set()

class RoadMap:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.tiles: List[List[MapTile]] = []
        self.tile_images: Dict[str, pygame.Surface] = {}
        self.load_tiles()

    def load_tiles(self) -> None:
        """Load all necessary tile images."""
        base_path = "assets/imgs/tiles/"

        for tile_name, tile_file in TILES.items():
            if any(prefix in tile_name for prefix in ["grass", "road"]):
                try:
                    img = pygame.image.load(f"{base_path}{tile_file}")
                    self.tile_images[tile_name] = pygame.transform.scale(img, TILE["size"])
                except pygame.error as e:
                    print(f"Warning: Could not load tile asset for {tile_name}: {e}")

    def init_empty_map(self) -> None:
        """Initialize empty map with grass tiles."""
        self.tiles = []

        for _ in range(self.rows):
            tile_row = []
            for _ in range(self.cols):
                tile = MapTile("grass_1")
                tile.img = self.tile_images["grass_1"]
                tile_row.append(tile)
            self.tiles.append(tile_row)

    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within screen boundries."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def generate_road_network(self) -> None:
        """Generate main road"""
        num_horizontal = random.randint(1, 2)
        num_vertical = random.randint(1, 2)

        # generate horizonal roads
        used_rows = set()
        for _ in range(num_horizontal):
            row = random.randint(2, self.rows - 3)
            while row in used_rows or row - 1 in used_rows or row + 1 in used_rows:
                row = random.randint(2, self.rows - 3)
            used_rows.add(row)

            for col in range(self.cols):
                self.tiles[row][col].roads.add(Direction.EAST)
                self.tiles[row][col].roads.add(Direction.WEST)

        # generate vertical roads
        used_cols = set()
        for _ in range(num_vertical):
            col = random.randint(2, self.cols - 3)
            while col in used_cols or col - 1 in used_cols or col + 1 in used_cols:
                col = random.randint(2, self.cols - 3)
            used_cols.add(col)

            for row in range(self.rows):
                self.tiles[row][col].roads.add(Direction.NORTH)
                self.tiles[row][col].roads.add(Direction.SOUTH)

    def get_tile_type(self, roads: Set[Direction]) -> str:
        """Determine appropiate tile type based on road connections"""
        if not roads:
            return random.choice(["grass_1", "grass_2"])

        # convert road directions to a pattern
        has_north = Direction.NORTH in roads
        has_south = Direction.SOUTH in roads
        has_east = Direction.EAST in roads
        has_west = Direction.WEST in roads

        # straight roads
        if has_north and has_south and not has_east and not has_west:
            return "grass_road_North"
        if has_east and has_west and not has_north and not has_south:
            return "grass_road_East"

        # corner roads
        if has_south and has_east and not has_north and not has_west:
            return "grass_road_CornerUL"
        if has_south and has_west and not has_north and not has_east:
            return "grass_road_CornerUR"
        if has_north and has_east and not has_south and not has_west:
            return "grass_road_CornerLL"
        if has_north and has_west and not has_south and not has_east:
            return "grass_road_CornerLR"

        # crossings
        if has_north and has_south and has_east and has_west:
            return "grass_road_Crossing"

        # T-junctions
        if has_north and has_south and has_east and not has_west:
            return "grass_road_SplitW"
        if has_north and has_south and not has_east and has_west:
            return "grass_road_SplitE"
        if has_north and not has_south and has_east and has_west:
            return "grass_road_SplitS"
        if not has_north and has_south and has_east and has_west:
            return "grass_road_SplitN"

        return "grass_1"
    
    def apply_tile_graphics(self) -> None:
        """Apply appropriate tile image based on road connections."""
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.tiles[row][col]
                tile.tile_type = self.get_tile_type(tile.roads)
                tile.img = self.tile_images[tile.tile_type]

    def generate_map(self) -> None:
        """Generate complete map with roads and appropriate tiles."""
        self.init_empty_map()
        self.generate_road_network()
        self.apply_tile_graphics()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the complete map."""
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.tiles[row][col]
                x = col * TILE["size"][0]
                y = row * TILE["size"][1]
                if tile.img is None:
                    raise ValueError(f"Tile `{tile.tile_type}` could not be loaded.")
                screen.blit(tile.img, (x, y))


class Bullet:
    def __init__(self, x: float, y: float, direction: str,  asset: str=BULLET["asset"]) -> None:
        self.x = x
        self.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 6

        self.img = pygame.image.load(asset)
        self.img = pygame.transform.scale(self.img, BULLET["size"])
        self.img = pygame.transform.rotate(self.img, BULLET_DIRECTION[direction])

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


class Tank:
    def __init__(
            self,
            x: float,
            y: float,
            bullet: type[Bullet]=Bullet,
            reload_time: int=500,
            asset: str=TANK["asset"],
            death_asset: str=TANK["asset"],
            health: int=6,
            bullet_asset: str=BULLET["asset"],
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

            bullet = self.bullet(bullet_center_x, bullet_center_y, self.direction, asset=self.bullet_asset)
            self.bullets.append(bullet)
            self.last_shot_time = pygame.time.get_ticks()

    def update_bullets(self) -> None:
        """Remove bullets that're out of screen"""
        self.bullets = [bullet for bullet in self.bullets if bullet.y > 0]

    def check_bullet_collision(self, tanks_list: List["Tank"]) -> None:
        """Check if the bullets hit any other tanks."""
        for bullet in self.bullets[:]:
            bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.img.get_width(), bullet.img.get_height())

            for tank in tanks_list:
                if tank == self:
                    continue

                tank_rect = pygame.Rect(tank.x, tank.y, tank.rect.width, tank.rect.height)

                if bullet_rect.colliderect(tank_rect):
                    self.bullets.remove(bullet)
                    tank.health -= 1
                    if tank.health <= 0:
                        tank.is_alive = False
                        tank.img = pygame.image.load(tank.death_asset)
                        tank.img = pygame.transform.scale(tank.img, TANK["size"])
                        tank.img = pygame.transform.rotate(tank.img, TANK_DIRECTION[tank.direction])
                    break

    def draw_health_bar(self, screen: pygame.Surface) -> None:
        """Draw the health bar with six boxes above the tank."""
        bar_width = 8
        bar_height = 8
        spacing = 2
        bar_x = self.x - (self.rect.width // 2) + (3 * (bar_width + spacing)) // 2  # center the bar above the tank
        bar_y = self.y - 20  # position above the tank

        fill_color = (239, 68, 68) # red
        outline_color = (15, 23, 42) # dark blue

        # draw the health boxes
        for i in range(self.health):
            box_rect = (bar_x + i * (bar_width + spacing), bar_y, bar_width, bar_height)
            # health box
            pygame.draw.rect(screen, fill_color, box_rect)
            # health outline box
            pygame.draw.rect(screen, outline_color, box_rect, 2)

    def draw(self, screen: pygame.Surface) -> None:
        """Paint the Tank and Bullets"""
        # draw the tank according to direction
        rotated_img = pygame.transform.rotate(self.img, TANK_DIRECTION[self.direction])
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


# setup the game
pygame.init()
screen = pygame.display.set_mode(GAME["screen_size"])
clock = pygame.time.Clock()

# objects
game_map = RoadMap(cols=15, rows=10)
game_map.generate_map()
player = Tank(
        x=300,
        y=200,
        asset="assets/imgs/tanks/tank_green.png",
        death_asset="assets/imgs/tanks/tank_green_body.png",
        bullet_asset="assets/imgs/tanks/bullet_green.png",
    )
enemy_1 = Tank(
        x=100,
        y=50,
        asset="assets/imgs/tanks/tank_red.png",
        death_asset="assets/imgs/tanks/tank_red_body.png",
        bullet_asset="assets/imgs/tanks/bullet_red.png",
    )
enemy_2 = Tank(
        x=200,
        y=50,
        asset="assets/imgs/tanks/tank_blue.png",
        death_asset="assets/imgs/tanks/tank_blue_body.png",
        bullet_asset="assets/imgs/tanks/bullet_blue.png",
    )
enemy_3 = Tank(
        x=300,
        y=50,
        asset="assets/imgs/tanks/tank_sand.png",
        death_asset="assets/imgs/tanks/tank_sand_body.png",
        bullet_asset="assets/imgs/tanks/bullet_sand.png",
    )

all_tanks = [enemy_1, enemy_2, player, enemy_3]

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
    game_map.draw(screen)

    # draw the tank and bullets
    all_tanks.sort(key=sort_alive_tanks_on_last) # show the alive tanks on top of the dead tanks
    for tank in all_tanks:
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

