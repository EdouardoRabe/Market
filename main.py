from connexion import ConnexionAccess

class Main:
    def __init__(self):
        self.connexion = ConnexionAccess()

    def run(self):
        if self.connexion.connect():
            print("Connection successful")
            rows = self.connexion.execute_query('SELECT * FROM box')
            if rows:
                for row in rows:
                    print(f"id: {row['id']}, name: {row['long']}")
            self.connexion.disconnect()
            print("Connection closed")
        else:
            print("Failed to connect to the database")


if __name__ == "__main__":
    teste = Main()
    teste.run()

 