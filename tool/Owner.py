from connexion import ConnexionAccess

class Owner:
    def __init__(self, idowner, name, firstname):
        self.__idowner = idowner
        self.__name = name
        self.__firstname = firstname

    def get_idowner(self):
        return self.__idowner

    def set_idowner(self, value):
        self.__idowner = value

    def get_name(self):
        return self.__name

    def set_name(self, value):
        self.__name = value

    def get_firstname(self):
        return self.__firstname

    def set_firstname(self, value):
        self.__firstname = value

    @staticmethod
    def getOwnerById(conn, idowner):
        query = "SELECT * FROM owners WHERE idowner = ?"
        result = conn.cursor().execute(query, (idowner,))
        row = result.fetchone()
        if row:
            return Owner(*row)
        return None

    @staticmethod
    def getOwners(conn):
        query = "SELECT * FROM owners"
        result = conn.cursor().execute(query)
        rows = result.fetchall()
        owners = [Owner(*row) for row in rows]
        return owners
