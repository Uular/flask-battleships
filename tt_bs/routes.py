from flask import jsonify, request, abort
import requests
from datetime import datetime

from tt_bs import app, db, limiter
from .models import Game, Square, Team

BASE_GAME = '/api/<string:game_name>/'

START_TIME = datetime(2017, 3, 16, 22, 00)

@app.route('/')
def hello_world():
    if (datetime.now() < START_TIME):
        return "Peli ei ole vielä alkanut!"
    return app.send_static_file('index.html')


@app.route(BASE_GAME)
def get_game(game_name):
    game = get_game_or_abort(game_name)
    teams = [team.as_dict() for team in Team.query.filter_by(game_name=game_name).all()]
    squares = [square.as_dict() for square in Square.query
                    .filter_by(game_name=game_name)
                    .filter(Square.shot_team_name != None).all()]
    width = game.width
    height = game.height
    return jsonify(name=game.name, teams=teams, squares=squares, width=width, height=height)

@app.route(BASE_GAME + 'squares', methods=['GET'])
def squares(game_name):
    game = get_game_or_abort(game_name)
    try:
        xmin = int(request.args['xmin'])
        ymin = int(request.args['ymin'])
        xmax = int(request.args['xmax'])
        ymax = int(request.args['ymax'])
        if xmin > xmax or ymin > ymax \
                or abs(xmin - xmax) * abs(ymin - ymax) > 100000:
            raise ValueError()
    except (KeyError, ValueError):
        abort(400)
        return

    squares = Square.query.filter(
        db.and_(Square.x.between(xmin, xmax),
                Square.y.between(ymin, ymax),
                Square.shot_team_name != None)
    ).all()
    return jsonify(squares=[square.as_dict() for square in squares])

@app.route(BASE_GAME + 'shoot', methods=['POST'])
@limiter.limit("10 per minute")
def shoot(game_name):
    game = get_game_or_abort(game_name)
    try:
        team_name = request.args['team']
        x = int(request.args['x'])
        y = int(request.args['y'])
        captcha = request.args['recaptcha_response_field']
    except (KeyError, ValueError):
        abort(400)
        return

    if not validate_captcha(captcha):
        abort(403, "Captcha validation failed")
        return


    team = get_team_or_abort(game_name, team_name)

    square = Square.query.filter_by(game=game, x=x, y=y).first()
    if square:
        if not square.shot_team and square.ship_team:
            square.game = game
            square.shot_team = team
            db.session.add(square)
            team.score += 1
            square.ship_team.score -= 1
            db.session.add(team)
            db.session.add(square.ship_team)
            db.session.commit()
            return jsonify(square=square.as_dict(), hit=True)
    else:
        square = Square(game, x, y, shot=team)
        db.session.add(square)
        db.session.commit()
    return jsonify(square=square.as_dict(), hit=False)

@app.route(BASE_GAME + 'teams', methods=['GET'])
def teams(game_name):
    game = get_game_or_abort(game_name)
    teams = Team.query.filter_by(game=game).all()
    return jsonify(teams=[team.as_dict() for team in teams])

def get_game_or_abort(game_name):
    game = Game.query.filter_by(name=game_name).first()
    if not game:
        abort(404, 'Game with name \'{}\' was not found'.format(game_name))
    else:
        return game


def get_team_or_abort(game_name, team_name):
    team = Team.query.filter_by(name=team_name, game_name=game_name).first()
    if not team:
        abort(404, 'Team with name \'{}\' was not found'.format(team_name))
    else:
        return team


def validate_captcha(captcha):
    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        "secret": app.config["RECAPTCHA_PRIVATE_KEY"],
        "response": captcha
    })

    response = r.json()
    return response['success']