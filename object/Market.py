from connexion import ConnexionAccess
from object import Box

class Market:
    def __init__(self, idmarket, long, larg, x, y,rent):
        self.idmarket= idmarket
        self.long = long
        self.larg= larg
        self.x = x
        self.y = y
        self.rent = rent
        
    @staticmethod
    def getMarkets():
        conn = ConnexionAccess.getConnexion()
        query = "SELECT * FROM market"
        result = conn.cursor().execute(query)
        rows = result.fetchall()
        markets = [Market(*row) for row in rows]
        return markets

    def getBoxs(self):
        conn = ConnexionAccess.getConnexion()
        query = "SELECT * FROM box WHERE idmarket = ?"
        result = conn.cursor().execute(query, (self.idmarket,))
        rows = result.fetchall()
        boxs = [Box(*row) for row in rows]
        return boxs
