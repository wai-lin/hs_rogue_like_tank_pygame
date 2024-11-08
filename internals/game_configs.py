"""
Game configurations.
"""

GAME = {
    "screen_size": (64 * 15, 64 * 10),
    "background": (0, 0, 0),
    "font": "assets/fonts/jersey_10/jersey10.ttf",
    "bots_count": 30,
    "bot_intervals": [1_000, 1_200, 800, 500, 300],
}

BULLET = {
    "asset": "assets/imgs/tanks/bullet_dark.png",
    "size": (8, 20),
    "shooting_sfx": "assets/sounds/lasergun.ogg",
}

BULLET_DIRECTION = {
    "UP": 0,
    "LEFT": 90,
    "DOWN": 180,
    "RIGHT": 270,
}

PLAYER_TANK = {
    "asset": "assets/imgs/tanks/tank_blue.png",
    "death_asset": "assets/imgs/tanks/tank_blue_body.png",
    "bullet_asset": "assets/imgs/tanks/bullet_blue.png",
    "size": (42, 46),
    "enemy_size": (31, 33),
}

BOT_TANK = {
    "asset": "assets/imgs/tanks/tank_red.png",
    "death_asset": "assets/imgs/tanks/tank_red_body.png",
    "size": (31, 33),
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
