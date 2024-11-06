"""
HighScore recorder
"""

import os
import json

from datetime import datetime
from typing import cast, Dict, Union, List

HighScoreEntry = Dict[str, Union[float, str]]
HighScores = List[HighScoreEntry]

HIGH_SCORE_FILE = "high_scores.json"
MAX_RECORDS = 5


def load_high_scores() -> HighScores:
    """Load all highscores"""
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return cast(HighScores, data.get("high_scores", []))
    return []


def save_high_scores(new_score: float):
    """Save high score record in json file"""
    high_scores = load_high_scores()
    new_entry: HighScoreEntry = {
        "score": new_score,
        "timestamp": datetime.now().isoformat(),
    }
    high_scores.append(new_entry)
    # record only latest records no more than MAX_RECORDS
    high_scores = sorted(
        high_scores, key=lambda entry: entry["timestamp"], reverse=True)[:MAX_RECORDS]

    with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as file:
        json.dump({"high_scores": high_scores}, file, indent=4)


def get_best_high_score(high_scores: HighScores) -> HighScoreEntry:
    """Get highest score from high scores and return default if empty."""
    if high_scores:
        return min(high_scores, key=lambda entry: entry["score"])
    return {"score": 0.0, "timestamp": ""}
