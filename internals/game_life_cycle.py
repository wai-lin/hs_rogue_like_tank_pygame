"""
Run the game in life-cycle.
"""

from typing import List, Union

import pygame

from .game_configs import GAME
from .player_tank import PlayerTank
from .bot_tank import generate_bots, MovableBotTank, is_player_won
from .high_scores import load_high_scores, get_best_high_score, save_high_scores
from .map_generator import draw_map
from .effects import draw_game_end_message


def game_life_cycle():
    """Runs the game in life-cycle."""

    pygame.init()

    # initialize base game
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(GAME["screen_size"])

    # generate game characters
    player_tank = PlayerTank(
        x=480,
        y=320,
        asset="assets/imgs/tanks/tank_green.png",
        death_asset="assets/imgs/tanks/tank_green_body.png",
        bullet_asset="assets/imgs/tanks/bullet_green.png",
        reload_time=300,
    )
    bot_tanks: List["MovableBotTank"] = generate_bots()
    all_tanks: List[Union["PlayerTank", "MovableBotTank"]] = [player_tank]
    all_tanks.extend(bot_tanks)

    # generate high score timer records
    is_high_score_saved = False
    high_scores = load_high_scores()
    best_high_score = float(get_best_high_score(high_scores)["score"])
    start_timer = pygame.time.get_ticks()
    end_timer: Union[int, None] = None

    is_game_running = True
    while is_game_running:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                is_game_running = False

        has_player_won = is_player_won(bot_tanks)

        # """Process player tank actions."""
        player_pressed_keys = pygame.key.get_pressed()
        if not has_player_won:
            player_tank.move_on_keypress(player_pressed_keys, all_tanks)
            if player_pressed_keys[pygame.K_SPACE]:
                player_tank.shoot()
            player_tank.process_bullet_collision(all_tanks)

        # """Map rendering"""
        screen.fill(GAME["background"])  # fill background color
        draw_map(screen)

        # """Render all tanks"
        for tank in all_tanks:
            # move bots in random movements
            if isinstance(tank, MovableBotTank):
                tank.move_randomly(all_tanks)
            # paint all tanks on screen
            tank.draw(screen)

        # """Game finished"""
        if has_player_won:
            elapsed_time = 0.0

            if end_timer is None:
                end_timer = pygame.time.get_ticks()

            if start_timer and end_timer:
                time_diff = end_timer - start_timer
                # convert milliseconds to seconds
                elapsed_time = time_diff / 1_000

                if elapsed_time < best_high_score:
                    best_high_score = elapsed_time
                if not is_high_score_saved:
                    is_high_score_saved = True
                    save_high_scores(elapsed_time)

            draw_game_end_message(
                screen=screen,
                elapsed_time=elapsed_time,
                high_scores=high_scores
            )

        pygame.display.flip()  # paint the screen
        clock.tick(60)  # cap FPS at 60

    pygame.quit()
