from connexion import ConnexionAccess
from material import Box

class Market:
    def __init__(self, idmarket, longueur, largeur, x, y, nommarket):
        self.__idmarket = idmarket
        self.__longueur = longueur
        self.__largeur = largeur
        self.__x = x
        self.__y = y
        self.__nommarket = nommarket

    def get_idmarket(self):
        return self.__idmarket

    def get_longueur(self):
        return self.__longueur

    def get_largeur(self):
        return self.__largeur

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y
    
    def get_nommarket(self):
        return self.__nommarket


    def set_idmarket(self, idmarket):
        self.__idmarket = idmarket

    def set_longueur(self, longueur):
        self.__longueur = longueur

    def set_largeur(self, largeur):
        self.__largeur = largeur

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y
        
    def set_nommarket(self, nommarket):
        self.__nommarket = nommarket

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
    
    @staticmethod
    def insertMarket(conn, longueur, largeur, x, y, nommarket):
        query = """
        INSERT INTO markets (longueur, largeur, x, y, nommarket) VALUES (?, ?, ?, ?, ?)
        """
        conn.cursor().execute(query, (longueur, largeur, x, y, nommarket))
        conn.commit()