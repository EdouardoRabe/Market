from connexion import ConnexionAccess
from tool import Periode, Rent, Paiement


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
        total_rent = area * rent_per_sqm.get_value()
        return total_rent
    
    def getPourcent(self, yearmonth):
        paiement = Paiement.getPaiement(yearmonth, self.__idbox)
        if paiement is None:
            return 0
        total_rent = self.calculRent(yearmonth)
        print(f"Total rent: { (paiement.get_value() / total_rent)}")
        return (paiement.get_value() / total_rent) 
    
    