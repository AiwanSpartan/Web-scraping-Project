from flask_restful import Resource
from models import gameData

class GameDataResource(Resource):
    def get(self):
        data = gameData.query.all()
        result = []
        for row in data:
            result.append({
                'name': row.name,
                "game_id" : row.gameID,
                'euro_orig': row.euro_orig,
                'reg_price': row.reg_price,
                'reg_euro': row.reg_euro
            })
        return result