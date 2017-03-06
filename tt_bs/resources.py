from .models import Game, Team, Square
from sqlite3 import IntegrityError


def get_game(game):
    return Game.query.filter_by(name=game).one()


def list_teams(game):
    teams = [team.name for team in Team.query.filter_by(game_name=game).all()]
    return teams


def get_squares(game):
    squares = Square.query.filter_by(game_name=game).all()
    squares_list = []
    for square in squares:
        square_obj = {
            'x': square.x,
            'y': square.y,
            'team': square.team_name
        }
        squares_list.append(square_obj)
    return squares_list


def shoot_square(x, y, team):
    pass

def add_team(db, name):
    team = Team(name)
    db.session.add(team)
    try:
        db.session.commit()
    except IntegrityError:
        return False
    else:
        return True


def add_ship(db, team, x, y):
    pass


def get_team(name):
    team = Team.query.filter_by(name=name).first()
    return team.name