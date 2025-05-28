from flask_restful import Resource
from models import gameData

class GameDataResource(Resource):
    def get(self):
        data = gameData.query.all()
        result = []
        for row in data:
            result.append
            ({
                'name': row.name,
                'prices': row.prices,
                "url" : row.url 
            })
        return result
