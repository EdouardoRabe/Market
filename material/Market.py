from connexion import ConnexionAccess
from material import Box

class Market:
    def __init__(self, idmarket, long, larg, x, y):
        self.__idmarket = idmarket
        self.__long = long
        self.__larg = larg
        self.__x = x
        self.__y = y
        self.__rent = 0.0

    def get_idmarket(self):
        return self.__idmarket

    def get_long(self):
        return self.__long

    def get_larg(self):
        return self.__larg

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_rent(self):
        return self.__rent

    def set_idmarket(self, idmarket):
        self.__idmarket = idmarket

    def set_long(self, long):
        self.__long = long

    def set_larg(self, larg):
        self.__larg = larg

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def set_rent(self, rent):
        self.__rent = rent

    @staticmethod
    def getMarkets(conn):
        query = "SELECT * FROM markets"
        result = conn.cursor().execute(query)
        rows = result.fetchall()
        markets = [Market(*row) for row in rows]
        return markets

    def getBoxs(self, conn):
        query = "SELECT * FROM boxs WHERE idmarket = ?"
        result = conn.cursor().execute(query, (self.__idmarket,))
        rows = result.fetchall()
        boxs = [Box(*row) for row in rows]
        return boxs