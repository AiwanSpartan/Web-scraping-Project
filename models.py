from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class gameData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gameID = db.Column(db.Integer, nullable=False)
    euro_orig = db.Column(db.Integer, nullable=False)
    reg_price = db.Column(db.Integer, nullable=False)
    reg_euro = db.Column(db.Integer, nullable=True)