"""
Rogue-Like Tank Game
"""

from internals import game_life_cycle

try:
    game_life_cycle()
except Exception as e:
    print(f"Game crashed! {e}")
