from tkinter import Tk
from app import MarketApp
from connexion import ConnexionAccess
from material import Market
from tool import Location, Paiement, Periode, Rent


if __name__ == "__main__":
    # m= Market.getMarkets()
    # bs= m[0].getBoxs()
    # b= bs[0]
    # print(b.isPaied("2025-01"))
    
    root = Tk()
    app = MarketApp(root)
    root.mainloop()
