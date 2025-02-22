import pyodbc

class ConnexionAccess:
    driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
    database_path = r'D:\ITU\Lecon\S4\Prog\Market\Base\base.accdb'
    
    @staticmethod
    def getConnexion():
        try:
            conn_str = f'DRIVER={ConnexionAccess.driver};DBQ={ConnexionAccess.database_path}'
            connection = pyodbc.connect(conn_str)
            return connection
        except pyodbc.Error as e:
            print(f"Error connecting to database: {e}")
            return None