from tt_bs import db


class Game(db.Model):
    __tablename__ = 'game'

    name = db.Column(db.String(255), primary_key=True)
    height = db.Column(db.Integer)
    width = db.Column(db.Integer)

    def __init__(self, name="titeta2017", height=10000, width=10000):
        self.name = name
        self.height = height
        self.width = width


class Team(db.Model):
    __tablename__ = 'team'

    name = db.Column(db.String(255), primary_key=True)
    game_name = db.Column(db.String(255))
    game = db.relationship("Game", foreign_keys=[game_name])

    def __init__(self, name=""):
        self.name = name


class Square(db.Model):
    __tablename__ = 'square'

    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, index=True, default=0)
    y = db.Column(db.Integer, index=True, default=0)

    game_name = db.Column(db.String(255))
    game = db.relationship("Game", foreign_keys=[game_name])

    ship_team_name = db.Column(db.String(255), db.ForeignKey('team.name'), nullable=True)
    ship_team = db.relationship("Team", foreign_keys=[ship_team_name])


    def __init__(self, x=0, y=0, team=None):
        self.x = x
        self.y = y
        self.team_name = team
