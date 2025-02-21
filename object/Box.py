from connexion import ConnexionAccess

class Box:
    def __init__(self, idbox, idmarket, long, larg, x, y, num):
        self.idbox = idbox
        self.idmarket = idmarket
        self.num = num
        self.long = long
        self.larg = larg
        self.x = x
        self.y = y