from flask import jsonify, request, abort
from tt_bs import app, db
from .models import Game, Square, Team

BASE_GAME = '/api/<string:game_name>/'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route(BASE_GAME)
def get_game(game_name):
    game = get_game_or_abort(game_name)
    teams = [team.as_dict() for team in Team.query.filter_by(game_name=game_name).all()]
    squares = [square.as_dict() for square in Square.query.filter_by(game_name=game_name)
        .filter(Square.shot_team_name != None).all()]
    return jsonify(name=game.name, teams=teams, squares=squares)


@app.route(BASE_GAME + 'shoot', methods=['POST'])
def shoot(game_name):
    game = get_game_or_abort(game_name)
    try:
        team_name = request.args['team']
        x = int(request.args['x'])
        y = int(request.args['y'])
    except (KeyError, ValueError):
        abort(400)
        return

    team = Team.query.filter_by(name=team_name).first()
    if not team:
        abort(404, "Team '{}' not found for this game".format(team_name))

    square = Square.query.filter_by(x=x, y=y).first()
    if square:
        if square.ship_team:
            if not square.shot_team:
                square.shot_team = team
                db.session.add(square)
                db.session.commit()
                return jsonify(square=square.as_dict(), hit=True), 200
            else:
                return jsonify(square=square.as_dict(), hit=False), 200
    return "", 204


def get_game_or_abort(game_name):
    game = Game.query.filter_by(name=game_name).first()
    if not game:
        abort(404, 'Game with name \'{}\' was not found'.format(game_name))
    else:
        return game


def get_team_or_abort(game_name, team_name):
    team = Game.query.filter_by(name=team_name, game_name=game_name).first()
    if not team:
        abort(404, 'Team with name \'{}\' was not found'.format(team_name))
