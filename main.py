from tkinter import Tk
from app import MarketApp
from material import Market
from tool import Periode


if __name__ == "__main__":
    p=Periode.getPeriode("2020-09")
    print(p.get_idperiode())
    # root = Tk()
    # app = MarketApp(root)
    # root.mainloop()