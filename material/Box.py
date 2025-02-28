import datetime
from dateutil.relativedelta import relativedelta
from connexion import ConnexionAccess
from tool import Location, Periode, Rent, Paiement

class Box:
    def __init__(self, idbox, idmarket, num, longueur, largeur, x, y):
        self.__idbox = idbox
        self.__idmarket = idmarket
        self.__num = num
        self.__longueur = longueur
        self.__largeur = largeur
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

    def get_longueur(self):
        return self.__longueur

    def set_longueur(self, value):
        self.__longueur = value

    def get_largeur(self):
        return self.__largeur

    def set_largeur(self, value):
        self.__largeur = value

    def get_x(self):
        return self.__x

    def set_x(self, value):
        self.__x = value

    def get_y(self):
        return self.__y

    def set_y(self, value):
        self.__y = value

    def showBox(self):
        print(f"{self.__idbox}\t{self.__idmarket}\t{self.__num}\t{self.__longueur}\t{self.__largeur}\t{self.__x}\t{self.__y}")

    @staticmethod
    def getBoxById(conn, idbox):
        query = "SELECT * FROM boxs WHERE idbox = ?"
        result = conn.cursor().execute(query, (idbox,))
        row = result.fetchone()
        if row:
            return Box(*row)
        return None
    
    @staticmethod
    def getBoxs(conn):
        query = "SELECT * FROM boxs"
        result = conn.cursor().execute(query)
        rows = result.fetchall()
        boxs = [Box(*row) for row in rows]
        return boxs

    def calculRent(self, conn, yearmonth):
        periode = Periode.getPeriode(conn, yearmonth)
        rent_per_sqm = Rent.getRent(conn ,self.__idmarket, periode.get_idperiode())
        area = self.__longueur * self.__largeur
        total_rent = area * rent_per_sqm.get_montant()
        return total_rent

    def getPourcent(self,conn, yearmonth):
        paiement = Paiement.getPaiement(conn,yearmonth, self.__idbox)
        if paiement is None:
            return 0
        total_rent = self.calculRent(conn , yearmonth)
        print(f"Total rent: { (paiement.get_montant() / total_rent)}")
        return (paiement.get_montant() / total_rent)

    def insertPaiement(self, conn,datepaiement, montant):
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
            last_payment = Paiement.getPaiement(conn, last_yearmonth, self.__idbox)
            last_paied_date =last_payment.get_paied()
            next_paied_date = last_paied_date + relativedelta(months=1)
            last_payment_montant = last_payment.get_montant()
            print(f"Last payment: {last_payment_montant}")
            rent = self.calculRent(conn,last_yearmonth)
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
            next_paied_date = datetime.datetime(2024, 1, 1)
        
        while montant > 0:
            yearmonth = next_paied_date.strftime('%Y-%m')
            rent = self.calculRent(conn,yearmonth)
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
        
    def isBoxRented(self,conn, yearmonth):
        location = Location.getLocationByBoxAndYearMonth(conn, self.__idbox, yearmonth)
        return location is not None
    
    @staticmethod
    def insertBox(conn, idmarket, num, longueur, largeur, x, y):
        query = """
            INSERT INTO boxs (idmarket, num, longueur, largeur, x, y)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        conn.cursor().execute(query, (idmarket, num, longueur, largeur, x, y))
        conn.commit()