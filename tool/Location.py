import sqlite3

from connexion import ConnexionAccess

class Location:
    def __init__(self, idlocation, idbox, idowner, debut, fin):
        self.__idlocation = idlocation
        self.__idbox = idbox
        self.__idowner = idowner
        self.__debut = debut
        self.__fin = fin

    def get_idlocation(self):
        return self.__idlocation

    def set_idlocation(self, value):
        self.__idlocation = value

    def get_idbox(self):
        return self.__idbox

    def set_idbox(self, value):
        self.__idbox = value

    def get_idowner(self):
        return self.__idowner

    def set_idowner(self, value):
        self.__idowner = value

    def get_debut(self):
        return self.__debut

    def set_debut(self, value):
        self.__debut = value

    def get_fin(self):
        return self.__fin

    def set_fin(self, value):
        self.__fin = value
        
    @staticmethod
    def getLocationByBoxAndYearMonth(idbox, yearmonth):
        conn = ConnexionAccess.getConnexion()
        query = """
        SELECT * FROM locations 
        WHERE idbox = ? AND ? BETWEEN FORMAT(debut, 'yyyy-mm') AND FORMAT(fin, 'yyyy-mm')
        """
        result = conn.cursor().execute(query, (idbox, yearmonth))
        row = result.fetchone()
        if row:
            return Location(*row)
        return None
