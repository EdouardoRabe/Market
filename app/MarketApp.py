import tkinter as tk
from material import Market, Box

class MarketApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()
        self.markets = Market.getMarkets()
        self.displayMarkets()

    def displayMarkets(self):
        for market in self.markets:
            self.displayMarket(market)

    def displayMarket(self, market):
        x, y = market.get_x(), market.get_y()
        long, larg = market.get_long(), market.get_larg()
        self.canvas.create_rectangle(x, y, x + long, y + larg, outline="blue", width=2)
        self.canvas.create_text(x + long / 2, y + larg / 2, text=f"Market ID: {market.get_idmarket()}", fill="blue")
        boxes = market.getBoxs()
        for box in boxes:
            self.displayBox(box)

    def displayBox(self, box):
        x, y = box.get_x(), box.get_y()
        long, larg = box.get_long(), box.get_larg()
        self.canvas.create_rectangle(x, y, x + long, y + larg, outline="red", width=2)
        self.canvas.create_text(x + long / 2, y + larg / 2, text=f"Box ID: {box.get_idbox()}", fill="red")
