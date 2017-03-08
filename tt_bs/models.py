from tt_bs import db
from sqlalchemy.ext.hybrid import hybrid_property


class Game(db.Model):
    __tablename__ = 'game'

    name = db.Column(db.String(255), primary_key=True)
    height = db.Column(db.Integer)
    width = db.Column(db.Integer)
    teams = db.relationship("Team", back_populates="game")
    squares = db.relationship("Square", back_populates="game")

    def __init__(self, name="titeta2017", height=10000, width=10000):
        self.name = name
        self.height = height
        self.width = width


class Team(db.Model):
    __tablename__ = 'team'

    name = db.Column(db.String(255), primary_key=True)
    game_name = db.Column(db.String(255), db.ForeignKey('game.name'), primary_key=True)
    game = db.relationship("Game", foreign_keys=[game_name], back_populates="teams")

    def __init__(self, game, name=""):
        self.game = game
        self.name = name

    @hybrid_property
    def points(self):
        return len(self.ships) + len(self.shots)

    def as_dict(self):
        return {
            'name': self.name,
            'points': self.points
        }


class Square(db.Model):
    __tablename__ = 'square'
    x = db.Column(db.Integer, primary_key=True)
    y = db.Column(db.Integer, primary_key=True)

    game_name = db.Column(db.String(255), db.ForeignKey('game.name'), primary_key=True)
    game = db.relationship("Game", back_populates="squares")

    ship_team_name = db.Column(db.String(255), db.ForeignKey('team.name'), nullable=False)
    ship_team = db.relationship("Team", foreign_keys=[ship_team_name], backref="ships")

    shot_team_name = db.Column(db.String(255), db.ForeignKey('team.name'), nullable=True)
    shot_team = db.relationship("Team", foreign_keys=[shot_team_name], backref="shots")

    def __init__(self, game, x=0, y=0, team=None):
        self.game = game
        x = max(min(x, game.width-1), 0)
        y = max(min(y, game.height-1), 0)
        self.x = x
        self.y = y
        self.ship_team = team

    def as_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'owner': self.ship_team_name,
            'shooter': self.shot_team_name
        }
