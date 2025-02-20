import pyodbc

class ConnexionAccess:
    driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
    database_path = r'C:\Users\edoua\Documents\Base de données1.accdb'
    connection = None
    cursor = None
    
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            conn_str = f'DRIVER={self.driver};DBQ={self.database_path}'
            self.connection = pyodbc.connect(conn_str)
            self.cursor = self.connection.cursor()
            return True
        except pyodbc.Error as e:
            print(f"Error connecting to database: {e}")
            return False

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except pyodbc.Error as e:
            print(f"Error executing query: {e}")
            return None