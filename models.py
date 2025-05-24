from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class gameData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    prices = db.Column(db.Float, nullable=False)
