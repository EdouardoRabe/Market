from connexion import ConnexionAccess

class Rent:
    def __init__(self, idrent, idmarket, idperiode, montant):
        self.__idrent = idrent
        self.__idmarket = idmarket
        self.__idperiode = idperiode
        self.__montant = montant

    def get_idrent(self):
        return self.__idrent

    def set_idrent(self, value):
        self.__idrent = value

    def get_idmarket(self):
        return self.__idmarket

    def set_idmarket(self, value):
        self.__idmarket = value

    def get_idperiode(self):
        return self.__idperiode

    def set_idperiode(self, value):
        self.__idperiode = value

    def get_montant(self):
        return self.__montant

    def set_montant(self, value):
        self.__montant = value

    @staticmethod
    def getRent(idmarket, idperiode):
        conn = ConnexionAccess.getConnexion()
        query = "SELECT * FROM rents WHERE idmarket = ? AND idperiode = ?"
        cursor = conn.cursor()
        cursor.execute(query, (idmarket, idperiode))
        row = cursor.fetchone()
        if row:
            return Rent(*row)
        return None