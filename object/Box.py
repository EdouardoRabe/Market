from connexion import ConnexionAccess

class Box:
    def __init__(self, idbox, idmarket, num, long, larg, x, y):
        self.idbox = idbox
        self.idmarket = idmarket
        self.num = num
        self.long = long
        self.larg = larg
        self.x = x
        self.y = y
    
    def showBox(self):
        print(f"{self.idbox}\t{self.idmarket}\t{self.num}\t{self.long}\t{self.larg}\t{self.x}\t{self.y}")

    def getBoxs(self):
        conn = ConnexionAccess.getConnexion()
        query = "SELECT * FROM boxs WHERE idmarket = ?"
        result = conn.cursor().execute(query, (self.idmarket,))
        rows = result.fetchall()
        boxs = [Box(*row) for row in rows]
        return boxs
