from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class gameData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gameID = db.Column(db.Integer, nullable=False)
    prices = db.relationship('Price', backref='game', lazy=True)

class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game_data.id'), nullable=False)