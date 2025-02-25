import datetime
from dateutil.relativedelta import relativedelta
from connexion import ConnexionAccess

class Paiement:
    def __init__(self, idpaiement, idbox, montant, paied, datepaiement):
        self.__idpaiement = idpaiement
        self.__idbox = idbox
        self.__montant = montant
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

    def get_montant(self):
        return self.__montant

    def set_montant(self, value):
        self.__montant = value

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
        query = """
            SELECT idbox, SUM(montant) as montant2, paied 
            FROM paiements 
            WHERE FORMAT(paied, 'yyyy-mm') = ? AND idbox = ? 
            GROUP BY idbox, paied
        """
        result = conn.cursor().execute(query, (yearmonth, idbox))
        row = result.fetchone()
        if row:
            idbox, montant2, paied = row
            return Paiement(0, idbox, montant2, paied, datetime.datetime.now())
        return None
   