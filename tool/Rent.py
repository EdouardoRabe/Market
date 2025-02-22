from connexion import ConnexionAccess

class Rent:
    idrent = None
    idmarket = None
    idperiode = None
    value = None

    def __init__(self, idrent, idmarket, idperiode, value):
        self._idrent = idrent
        self._idmarket = idmarket
        self._idperiode = idperiode
        self._value = value

    def get_idrent(self):
        return self._idrent

    def set_idrent(self, value):
        self._idrent = value

    def get_idmarket(self):
        return self._idmarket

    def set_idmarket(self, value):
        self._idmarket = value

    def get_idperiode(self):
        return self._idperiode

    def set_idperiode(self, value):
        self._idperiode = value

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value


    @staticmethod
    def getRent(idmarket, idperiode):
        conn = ConnexionAccess.getConnexion()
        query = "SELECT idrent, idmarket, idperiode, value FROM rents WHERE idmarket = ? AND idperiode = ?"
        cursor = conn.cursor()
        cursor.execute(query, (idmarket, idperiode))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Rent(row[0], row[1], row[2], row[3])
        else:
            return None