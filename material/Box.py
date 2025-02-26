import datetime
from dateutil.relativedelta import relativedelta
from connexion import ConnexionAccess
from tool import Location, Periode, Rent, Paiement

class Box:
    def __init__(self, idbox, idmarket, num, long, larg, x, y):
        self.__idbox = idbox
        self.__idmarket = idmarket
        self.__num = num
        self.__long = long
        self.__larg = larg
        self.__x = x
        self.__y = y

    def get_idbox(self):
        return self.__idbox

    def set_idbox(self, value):
        self.__idbox = value

    def get_idmarket(self):
        return self.__idmarket

    def set_idmarket(self, value):
        self.__idmarket = value

    def get_num(self):
        return self.__num

    def set_num(self, value):
        self.__num = value

    def get_long(self):
        return self.__long

    def set_long(self, value):
        self.__long = value

    def get_larg(self):
        return self.__larg

    def set_larg(self, value):
        self.__larg = value

    def get_x(self):
        return self.__x

    def set_x(self, value):
        self.__x = value

    def get_y(self):
        return self.__y

    def set_y(self, value):
        self.__y = value

    def showBox(self):
        print(f"{self.__idbox}\t{self.__idmarket}\t{self.__num}\t{self.__long}\t{self.__larg}\t{self.__x}\t{self.__y}")

    @staticmethod
    def getBoxById(idbox):
        conn = ConnexionAccess.getConnexion()
        query = "SELECT * FROM boxs WHERE idbox = ?"
        result = conn.cursor().execute(query, (idbox,))
        row = result.fetchone()
        if row:
            return Box(*row)
        return None
    
    @staticmethod
    def getBoxs():
        conn = ConnexionAccess.getConnexion()
        query = "SELECT * FROM boxs"
        result = conn.cursor().execute(query)
        rows = result.fetchall()
        boxs = [Box(*row) for row in rows]
        return boxs

    def calculRent(self, yearmonth):
        periode = Periode.getPeriode(yearmonth)
        rent_per_sqm = Rent.getRent(self.__idmarket, periode.get_idperiode())
        area = self.__long * self.__larg
        total_rent = area * rent_per_sqm.get_montant()
        return total_rent

    def getPourcent(self, yearmonth):
        paiement = Paiement.getPaiement(yearmonth, self.__idbox)
        if paiement is None:
            return 0
        total_rent = self.calculRent(yearmonth)
        print(f"Total rent: { (paiement.get_montant() / total_rent)}")
        return (paiement.get_montant() / total_rent)

    def insertPaiement(self, datepaiement, montant):
        conn = ConnexionAccess.getConnexion()
        cursor = conn.cursor()
        montant = float(montant)
        query = """
            SELECT TOP 1 FORMAT(paied, 'yyyy-MM') as yearmonth 
            FROM paiements 
            WHERE idbox = ? 
            ORDER BY paied DESC
        """
        result = cursor.execute(query, (self.__idbox,))
        last_yearmonth = result.fetchone()
        
        if last_yearmonth:
            last_yearmonth = last_yearmonth[0]
            last_payment = Paiement.getPaiement(last_yearmonth, self.__idbox)
            last_paied_date =last_payment.get_paied()
            next_paied_date = last_paied_date + relativedelta(months=1)
            last_payment_montant = last_payment.get_montant()
            print(f"Last payment: {last_payment_montant}")
            rent = self.calculRent(last_yearmonth)
            if last_payment_montant < rent:
                remaining_rent = rent - last_payment_montant
                if montant >= remaining_rent:
                    query = "INSERT INTO paiements (idbox, montant, paied, datepaiement) VALUES (?, ?, ?, ?)"
                    cursor.execute(query, (self.__idbox, remaining_rent, last_paied_date.strftime('%Y-%m-%d'), datepaiement))
                    montant -= remaining_rent
                else:
                    query = "INSERT INTO paiements (idbox, montant, paied, datepaiement) VALUES (?, ?, ?, ?)"
                    cursor.execute(query, (self.__idbox, montant, last_paied_date.strftime('%Y-%m-%d'), datepaiement))
                    montant = 0
        else:
            next_paied_date = datetime.datetime(2025, 1, 1)
        
        while montant > 0:
            yearmonth = next_paied_date.strftime('%Y-%m')
            rent = self.calculRent(yearmonth)
            if montant >= rent:
                query = "INSERT INTO paiements (idbox, montant, paied, datepaiement) VALUES (?, ?, ?, ?)"
                cursor.execute(query, (self.__idbox, rent, next_paied_date.strftime('%Y-%m-%d'), datepaiement))
                montant -= rent
                next_paied_date += relativedelta(months=1)
            else:
                query = "INSERT INTO paiements (idbox, montant, paied, datepaiement) VALUES (?, ?, ?, ?)"
                cursor.execute(query, (self.__idbox, montant, next_paied_date.strftime('%Y-%m-%d'), datepaiement))
                montant = 0
        
        conn.commit()
        cursor.close()
        conn.close()
        
    def isBoxRented(self, yearmonth):
        location = Location.getLocationByBoxAndYearMonth(self.__idbox, yearmonth)
        return location is not None
        