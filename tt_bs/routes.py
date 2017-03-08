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
    squares = [square.as_dict() for square in Square.query.filter_by(game_name=game_name).filter(Square.shot_team_name != None).all()]
    return jsonify(name=game.name, teams=teams, squares=squares)


@app.route(BASE_GAME + 'shoot', methods=['POST'])
def shoot(game_name):
    game = get_game_or_abort(game_name)
    try:
        team = request.args['team']
        x = request.args['x']
        y = request.args['y']
    except KeyError:
        abort(400)
        return

    square = Square.query.filter_by(x=x, y=y).first()
    if square:
        if square.ship_team and square.shot_team:
            pass

def get_game_or_abort(game_name):
    game = Game.query.filter_by(name=game_name).first()
    if not game:
        abort(404, 'Game with name \'{}\' was not found'.format(game_name))
    else:
        return game

@app.errorhandler(404)
def error_404(error):
    response = jsonify(error=404, message=error.description)
    return response, 404