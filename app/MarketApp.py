import tkinter as tk
from material import Market, Box

class MarketApp:
    def __init__(self, root):
        self.root = root
        self.yearmonth = tk.StringVar(value="2023-01")
        self.yearmonth.trace("w", self.update_title)
        
        self.title_label = tk.Label(root, text="Situation de Marché au mois de", font=("Helvetica", 16))
        self.title_label.pack(pady=5)
        
        self.date_frame = tk.Frame(root)
        self.date_frame.pack(pady=5)
        
        self.date_label = tk.Label(self.date_frame, text="Date:")
        self.date_label.pack(side=tk.LEFT)
        
        self.date_entry = tk.Entry(self.date_frame, textvariable=self.yearmonth)
        self.date_entry.pack(side=tk.LEFT)
        
        self.validate_button = tk.Button(root, text="Valider", command=self.validate_date)
        self.validate_button.pack(pady=5)
        
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()
        
        self.markets = Market.getMarkets()
        self.update_title()
        self.displayMarkets()

    def update_title(self, *args):
        date_value = self.yearmonth.get()
        self.title_label.config(text=f"Situation de Marché au mois de {date_value}")

    def validate_date(self):
        self.canvas.delete("all")
        self.displayMarkets()

    def displayMarkets(self):
        for market in self.markets:
            self.displayMarket(market)

    def displayMarket(self, market):
        x, y = market.get_x(), market.get_y()
        long, larg = market.get_long(), market.get_larg()
        self.canvas.create_rectangle(x, y, x + long, y + larg, outline="blue", width=2)
        self.canvas.create_text(x + long / 2, y - 10, text=f"Market ID: {market.get_idmarket()}", fill="blue")
        boxes = market.getBoxs()
        for box in boxes:
            self.displayBox(box)

    def displayBox(self, box):
        x, y = box.get_x(), box.get_y()
        long, larg = box.get_long(), box.get_larg()
        yearmonth = self.yearmonth.get()
        percent_paid = box.getPourcent(yearmonth)
        green_width = int(long * percent_paid)
        red_width = long - green_width
        if green_width > 0:
            self.canvas.create_rectangle(x, y, x + green_width, y + larg, outline="green", fill="green", width=2)
        if red_width > 0:
            self.canvas.create_rectangle(x + green_width, y, x + long, y + larg, outline="red", fill="red", width=2)
        self.canvas.create_text(x + long / 2, y + larg / 2, text=f"Box ID: {box.get_idbox()}", fill="white")
