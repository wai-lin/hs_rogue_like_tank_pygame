"""
Tank game
"""

import pygame
import math

# game config
GAME = {
    "screen_size": (64 * 15, 64 * 10),
    "background": (0, 0, 0),
}

TILE = {
    "asset": "assets/PNG/Retina/tileSand1.png",
    "size": (64, 64),
}

BULLET = {
    "asset": "assets/PNG/Retina/bulletDark1_outline.png",
    "size": (8, 20)
}

BULLET_DIRECTION = {
    "UP": 0,
    "LEFT": 90,
    "DOWN": 180,
    "RIGHT": 270,
}

TANK = {
    "asset": "assets/PNG/Retina/tank_dark.png",
    "size": (42, 46),
}

TANK_DIRECTION = {
    "DOWN": 0,
    "RIGHT": 90,
    "UP": 180,
    "LEFT": 270,
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
    def __init__(self, x: float, y: float, bullet=Bullet, reload_time=500, asset: str=TANK["asset"], health: int=6, bullet_asset: str=BULLET["asset"]) -> None:
        self.x = x
        self.y = y
        self.speed = 2
        self.direction = "UP"
        self.initial_direction = None
        self.health = health

        self.img = pygame.image.load(asset)
        self.img = pygame.transform.scale(self.img, TANK["size"])
        self.rect = self.img.get_rect(center=(400, 300))

        self.bullet_asset = bullet_asset
        self.bullet = bullet
        self.bullets: list["Bullet"] = []
        self.last_shot_time = 0
        self.bullet_speed = 6
        self.cooldown = reload_time

    def move_on_keypress(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Movement handler for keys input."""
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

        # restrict movement to screen boundries
        screen_width, screen_height = GAME["screen_size"]

        # check horizonal boundries
        new_x_pos = self.x + move_x
        if 0 <= new_x_pos <= screen_width - self.rect.width:
            self.x = new_x_pos

        # check vertical boundries
        new_y_pos = self.y + move_y
        if 0 <= new_y_pos <= screen_height - self.rect.height:
            self.y += move_y

        # reset starting direction if no key pressed
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.initial_direction = None

    def move(self, direction: str) -> None:
        """Move tank according to key press direction."""
        self.direction = direction
        rad_angle = math.radians(TANK_DIRECTION[direction])
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

            bullet = self.bullet(bullet_center_x, bullet_center_y, self.direction, asset=self.bullet_asset)
            self.bullets.append(bullet)
            self.last_shot_time = pygame.time.get_ticks()

    def update_bullets(self) -> None:
        """Remove bullets that're out of screen"""
        self.bullets = [bullet for bullet in self.bullets if bullet.y > 0]

    def check_bullet_collision(self, tanks_list: list["Tank"]) -> None:
        """Check if the bullets hit any other tanks."""
        for bullet in self.bullets[:]:
            bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.img.get_width(), bullet.img.get_height())

            for tank in tanks_list:
                if tank == self:
                    continue

                tank_rect = pygame.Rect(tank.x, tank.y, tank.rect.width, tank.rect.height)

                if bullet_rect.colliderect(tank_rect):
                    self.bullets.remove(bullet)
                    print(f"Hit tank at position x:{tank.x}, y:{tank.y}")
                    tank.health -= 1
                    print(f"Tank health {tank.health}")
                    if tank.health <= 0:
                        print(f"Tank destroyed: {tank}")
                        tanks_list.remove(tank)
                    break

    def draw(self, screen: pygame.Surface) -> None:
        """Paint the Tank and Bullets"""
        # draw the tank according to direction
        rotated_img = pygame.transform.rotate(self.img, TANK_DIRECTION[self.direction])
        center = (self.x + self.rect.width / 2, self.y + self.rect.height / 2)
        rotated_rect = rotated_img.get_rect(center=center)
        screen.blit(rotated_img, rotated_rect.topleft)

        # display health above tank
        font = pygame.font.SysFont("BlexMono Nerd Font", 16)
        health_text = font.render(f"HP: {self.health}", True, (255, 0, 0))
        screen.blit(health_text, (self.x, self.y - 20))

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
tile = Tile()
player = Tank(
        x=300,
        y=400,
        asset="assets/PNG/Retina/tank_green.png",
        bullet_asset="assets/PNG/Retina/bulletGreen1_outline.png",
    )
enemy_1 = Tank(
        x=100,
        y=50,
        asset="assets/PNG/Retina/tank_red.png",
        bullet_asset="assets/PNG/Retina/bulletRed1_outline.png",
    )
enemy_2 = Tank(
        x=200,
        y=50,
        asset="assets/PNG/Retina/tank_blue.png",
        bullet_asset="assets/PNG/Retina/bulletBlue1_outline.png",
    )
enemy_3 = Tank(
        x=300,
        y=50,
        asset="assets/PNG/Retina/tank_sand.png",
        bullet_asset="assets/PNG/Retina/bulletSand1.png",
    )

all_tanks = [player, enemy_1, enemy_2, enemy_3]

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
    player.move_on_keypress(keys)
    if keys[pygame.K_SPACE]:
        player.shoot()
    player.check_bullet_collision(all_tanks)

    """
    Screen painting
    """
    # fill background color
    screen.fill(GAME["background"])
    # draw tiles
    tile.draw_tiles(screen, 20, 25)

    # draw the tank and bullets
    player.draw(screen)
    enemy_1.draw(screen)
    enemy_2.draw(screen)
    enemy_3.draw(screen)

    """
    Wrap-Ups
    """
    # update the display
    pygame.display.flip()
    # cap the fps at 60
    clock.tick(60)

# exit game
pygame.quit()

