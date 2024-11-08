"""
Rogue-Like Tank Game
"""
import logging
import traceback

from internals import game_life_cycle

try:
    game_life_cycle()
except Exception as e:
    print(f"Game crashed! {e}")
    logging.error(traceback.format_exc())
