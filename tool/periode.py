from connexion import ConnexionAccess

class Periode:
    def __init__(self, idperiode, debut, fin):
        self.__idperiode = idperiode
        self.__debut = debut
        self.__fin = fin

    def get_idperiode(self):
        return self.__idperiode

    def get_debut(self):
        return self.__debut

    def get_fin(self):
        return self.__fin

    def set_idperiode(self, idperiode):
        self.__idperiode = idperiode

    def set_debut(self, debut):
        self.__debut = debut

    def set_fin(self, fin):
        self.__fin = fin

    @staticmethod
    def getPeriode(conn, yearMonth):
        month = int(yearMonth.split('-')[1])
        query = "SELECT idperiode, debut, fin FROM periodes WHERE ? BETWEEN debut AND fin"
        cursor = conn.cursor()
        cursor.execute(query, (month,))
        row = cursor.fetchone()
        if row:
            return Periode(row[0], row[1], row[2])
        else:
            return None