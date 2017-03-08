import random
import sqlalchemy

from tt_bs import app, db
from tt_bs.models import Game, Team, Square

import game_setup as gs

UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3

game = Game.query.filter_by(name=gs.GAME_NAME).first()
if not game:
    game = Game(name=gs.GAME_NAME, height=gs.HEIGHT, width=gs.WIDTH)
    db.session.add(game)
    db.session.commit()

for team_name in gs.TEAMS:
    team = Team.query.filter_by(name=team_name).first()
    if not team:
        team = Team(game, team_name)
        db.session.add(team)
        db.session.commit()

    for ship_size in gs.SHIPS:
        start_x = random.randint(ship_size-1, gs.WIDTH-ship_size)
        start_y = random.randint(ship_size-1, gs.HEIGHT-ship_size)
        orientation = random.choice(["x", "y"])
        x_pos = [start_x] * ship_size
        y_pos = [start_y] * ship_size
        if orientation == "x":
            x_pos = [start_x + i for i in range(ship_size)]
        else:
            y_pos = [start_y + i for i in range(ship_size)]

        for x, y in zip(x_pos, y_pos):
            square = Square(game, x, y, team=team)
            db.session.add(square)
        db.session.commit()

