from connexion import ConnexionAccess

class Periode:
    def __init__(self, idperiode, depuis):
        self.__idperiode = idperiode
        self.__depuis = depuis

    def get_idperiode(self):
        return self.__idperiode

    def get_depuis(self):
        return self.__depuis

    def set_idperiode(self, idperiode):
        self.__idperiode = idperiode

    def set_depuis(self, depuis):
        self.__depuis = depuis

    @staticmethod
    def getPeriode(conn, yearMonth):
        query = """
            SELECT TOP 1 idperiode, depuis 
            FROM periodes 
            WHERE FORMAT(depuis, 'yyyy-MM') <= ? 
            ORDER BY depuis DESC
        """
        cursor = conn.cursor()
        cursor.execute(query, (yearMonth,))
        row = cursor.fetchone()
        if row:
            return Periode(row[0], row[1].strftime('%Y-%m'))
        else:
            return Periode(1, None)
    
    
