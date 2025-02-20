from connexion import ConnexionAccess

class Main:
    def __init__(self):
        self.connexion = ConnexionAccess()

    def run(self):
        if self.connexion.connect():
            print("Connection successful")
            rows = self.connexion.execute_query('SELECT * FROM TesteTable')
            if rows:
                for row in rows:
                    print(f"id: {row['Teste']}, name: {row['Field1']}")
            self.connexion.disconnect()
            print("Connection closed")
        else:
            print("Failed to connect to the database")


if __name__ == "__main__":
    teste = Main()
    teste.run()

 