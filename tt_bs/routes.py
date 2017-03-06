from flask import jsonify, request, abort
from tt_bs import app, db
from .resources import list_teams, shoot_square, get_game
from .models import Game

BASE_GAME = '/api/<string:game_name>/'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route(BASE_GAME)
def game(game_name):
    game = get_game_or_abort(game_name)
    return game


@app.route(BASE_GAME + 'teams', methods=['GET'])
def get_squares(game_name):
    game = get_game_or_abort(game_name)
    return jsonify(type='teams', list=list_teams(game))


@app.route(BASE_GAME + 'squares', methods=['GET', 'POST'])
def shoot():
    game = get_game_or_abort(game_name)
    if request.method == 'POST':
        try:
            team = request.args['team']
            x = request.args['x']
            y = request.args['y']
        except KeyError:
            abort(400)
        shot_square = Square()
    else:
        pass


def get_game_or_abort(game):
    game = get_game(game)
    if not game:
        abort(404)
    else:
        return game