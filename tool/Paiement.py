from connexion import ConnexionAccess

class Paiement:
    def __init__(self, idpaiement, idbox, value, paied, datepaiement):
        self.__idpaiement = idpaiement
        self.__idbox = idbox
        self.__value = value
        self.__paied = paied
        self.__datepaiement = datepaiement

    def get_idpaiement(self):
        return self.__idpaiement

    def set_idpaiement(self, value):
        self.__idpaiement = value

    def get_idbox(self):
        return self.__idbox

    def set_idbox(self, value):
        self.__idbox = value

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value

    def get_paied(self):
        return self.__paied

    def set_paied(self, value):
        self.__paied = value

    def get_datepaiement(self):
        return self.__datepaiement

    def set_datepaiement(self, value):
        self.__datepaiement = value

    @staticmethod
    def getPaiements():
        conn = ConnexionAccess.getConnexion()
        query = "SELECT * FROM paiements"
        result = conn.cursor().execute(query)
        rows = result.fetchall()
        paiements = [Paiement(*row) for row in rows]
        return paiements
    
    @staticmethod
    def getPaiement(yearmonth, idbox):
        conn = ConnexionAccess.getConnexion()
        query = "SELECT * FROM paiements WHERE FORMAT(paied, 'yyyy-mm') = ? AND idbox = ?"
        result = conn.cursor().execute(query, (yearmonth, idbox))
        row = result.fetchone()
        if row:
            return Paiement(*row)
        return None