from connexion import ConnexionAccess
from object import Box

class Market:
    def __init__(self, idmarket, long, larg, x, y):
        self.idmarket= idmarket
        self.long = long
        self.larg= larg
        self.x = x
        self.y = y
        self.rent = 0.0
        
    @staticmethod
    def getMarkets():
        conn = ConnexionAccess.getConnexion()
        query = "SELECT * FROM markets"
        result = conn.cursor().execute(query)
        rows = result.fetchall()
        markets = [Market(*row) for row in rows]
        return markets

    def getBoxs(self):
        conn = ConnexionAccess.getConnexion()
        query = "SELECT * FROM boxs WHERE idmarket = ?"
        result = conn.cursor().execute(query, (self.idmarket,))
        rows = result.fetchall()
        boxs = [Box(*row) for row in rows]
        return boxs
