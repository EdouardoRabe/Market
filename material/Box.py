from connexion import ConnexionAccess

class Box:
    def __init__(self, idbox, idmarket, num, long, larg, x, y):
        self.__idbox = idbox
        self.__idmarket = idmarket
        self.__num = num
        self.__long = long
        self.__larg = larg
        self.__x = x
        self.__y = y
    
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
