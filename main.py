from tkinter import Tk
from app import MarketApp
from material import Market


if __name__ == "__main__":
    root = Tk()
    app = MarketApp(root)
    root.mainloop()