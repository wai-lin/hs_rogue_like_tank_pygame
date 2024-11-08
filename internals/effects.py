"""
Game effects.
Sound, Text, etc...
"""

from typing import Tuple
from datetime import datetime

import pygame

from .game_configs import GAME, BULLET
from .high_scores import HighScores

pygame.mixer.init()
pygame.font.init()

SHOOTING_SFX = pygame.mixer.Sound(BULLET["shooting_sfx"])

TITLE_FONT = pygame.font.Font(GAME["font"], 74)
TEXT_FONT = pygame.font.Font(GAME["font"], 40)


def draw_text_with_outline(
    text: str,
    font: pygame.font.Font,
    color: Tuple[int, int, int],
    outline_color: Tuple[int, int, int],
    position: Tuple[int, int],
    screen: pygame.Surface,
):
    """Text with outline renderer."""
    outline_positions = [
        (position[0] - 1, position[1] - 1),
        (position[0] + 1, position[1] - 1),
        (position[0] - 1, position[1] + 1),
        (position[0] + 1, position[1] + 1),
    ]
    for pos in outline_positions:
        outline_surface = font.render(text, True, outline_color)
        screen.blit(outline_surface, pos)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)


def draw_game_end_message(
    screen: pygame.Surface,
    elapsed_time: float,
    high_scores: HighScores,
):
    """End game with final message."""

    # show winning screen
    text_surface = TITLE_FONT.render("You Won!", True, (0, 0, 128))
    text_rect = text_surface.get_rect(
        center=(GAME["screen_size"][0] // 2, GAME["screen_size"][1] // 2 - 100))
    screen.blit(text_surface, text_rect)

    time_text = f"Your score: {elapsed_time:.2f} seconds"
    time_surface = TITLE_FONT.render(time_text, True, (0, 0, 128))
    time_rect = time_surface.get_rect(
        center=(GAME["screen_size"][0] // 2, GAME["screen_size"][1] // 2 + - 40))
    screen.blit(time_surface, time_rect)

    # list high scores
    for i, high_score in enumerate(high_scores):
        timestamp = datetime.fromisoformat(str(high_score["timestamp"]))
        # Format to "DD-MM-YYYY HH:MM AM/PM"
        formatted_timestamp = timestamp.strftime("%d-%m-%Y %I:%M %p")

        label_text = f"#{i+1} {formatted_timestamp}"
        score_text = f"{high_score['score']:.2f} seconds"
        high_score_text = f"{label_text} : {score_text}"
        draw_text_with_outline(
            text=high_score_text,
            font=TEXT_FONT,
            color=(255, 255, 255),
            outline_color=(60, 60, 60),
            position=(GAME["screen_size"][0] // 4,
                      GAME["screen_size"][1] // 2 + 40 + i * 30),
            screen=screen,
        )
