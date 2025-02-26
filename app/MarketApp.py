import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from connexion import ConnexionAccess
from material import Market, Box
import threading
import webbrowser
import os
import sys
from tkinter import messagebox
from datetime import datetime

class MarketApp:
    def __init__(self, root):
        self.conn = ConnexionAccess.getConnexion()
        self.root = root
        self.root.title("Market Management App")
        self.root.geometry("800x700")
        style = ttk.Style()
        style.configure("TLabel", background="#F0F8FF", foreground="#333333", font=("Arial", 12))
        style.configure("TButton", background="#5A9", foreground="#000000", font=("Arial", 12), padding=(8, 4), borderwidth=0, relief="flat")
        style.map("TButton", background=[("active", "#4A8")], foreground=[("active", "#000000")])
        style.configure("TEntry", fieldbackground="#FFFFFF", foreground="#333333", font=("Arial", 12), padding=5, borderwidth=2, relief="solid", bordercolor="#CCCCCC")
        self.root.configure(bg="#F0F8FF")
        self.yearmonth = tk.StringVar(value="2025-01")
        self.yearmonth.trace("w", self.update_title)
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)
        self.menu_bar.add_command(label="Home", command=self.show_home)
        self.menu_bar.add_command(label="Paiement sur Tkinter", command=self.show_payments)
        self.menu_bar.add_command(label="Paiement sur web", command=self.open_web_app)
        self.home_frame = tk.Frame(root, bg="#F0F8FF")
        self.payment_frame = tk.Frame(root, bg="#F0F8FF")
        self.init_home_page()
        self.init_payment_page()
        self.show_home()
        self.root.protocol("WM_DELETE_WINDOW", self.close_connection)

    def init_home_page(self):
        self.title_label = ttk.Label(self.home_frame, text="Situation de Marché au mois de", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=5)
        self.date_frame = tk.Frame(self.home_frame, bg="#F0F8FF")
        self.date_frame.pack(pady=5)
        self.date_label = ttk.Label(self.date_frame, text="Date:")
        self.date_label.pack(side=tk.LEFT, padx=5)
        self.date_entry = ttk.Entry(self.date_frame, textvariable=self.yearmonth, width=10, style="TEntry")
        self.date_entry.pack(side=tk.LEFT, padx=5)
        self.validate_button = ttk.Button(self.home_frame, text="Valider", command=self.validate_date, style="TButton")
        self.validate_button.pack(pady=5)
        self.top_frame = tk.Frame(self.home_frame, bg="#F0F8FF")
        self.top_frame.pack(fill=tk.BOTH, expand=True)
        self.bottom_frame = tk.Frame(self.home_frame, bg="#F0F8FF")
        self.bottom_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.bottom_frame, width=800, height=600, bg="#F0F8FF")
        self.canvas.pack()
        self.markets = Market.getMarkets(self.conn)
        self.update_title()
        self.displayMarkets()

    def init_payment_page(self):
        self.payment_label = ttk.Label(self.payment_frame, text="Faire un paiement", font=("Arial", 16, "bold"))
        self.payment_label.pack(pady=5)
        
        self.box_label = ttk.Label(self.payment_frame, text="Box:")
        self.box_label.pack(pady=5)
        self.box_var = tk.StringVar()
        self.box_select = ttk.Combobox(self.payment_frame, textvariable=self.box_var)
        self.box_select['values'] = [box.get_idbox() for box in Box.getBoxs(self.conn)]
        self.box_select.pack(pady=5)
        
        self.date_label = ttk.Label(self.payment_frame, text="Date de paiement:")
        self.date_label.pack(pady=5)
        self.date_var = tk.StringVar()
        self.date_entry = DateEntry(self.payment_frame, textvariable=self.date_var, date_pattern='yyyy-mm-dd')
        self.date_entry.pack(pady=5)
        
        self.amount_label = ttk.Label(self.payment_frame, text="Montant:")
        self.amount_label.pack(pady=5)
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(self.payment_frame, textvariable=self.amount_var)
        self.amount_entry.pack(pady=5)
        
        self.payment_button = ttk.Button(self.payment_frame, text="Process Payment", command=self.process_payment)
        self.payment_button.pack(pady=5)

    def show_home(self):
        self.payment_frame.pack_forget()
        self.home_frame.pack(fill=tk.BOTH, expand=True)

    def show_payments(self):
        self.home_frame.pack_forget()
        self.payment_frame.pack(fill=tk.BOTH, expand=True)

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
        self.canvas.create_rectangle(x, y, x + long, y + larg, outline="#5A9", width=2)
        self.canvas.create_text(x + long / 2, y - 10, text=f"Market ID: {market.get_idmarket()}", fill="#5A9", font=("Helvetica", 10, "bold"))
        boxes = market.getBoxs(self.conn)
        for box in boxes:
            self.displayBox(box)

    def displayBox(self, box):
        x, y = box.get_x(), box.get_y()
        long, larg = box.get_long(), box.get_larg()
        yearmonth = self.yearmonth.get()
        percent_paid = box.getPourcent(self.conn, yearmonth)
        green_width = int(long * percent_paid)
        red_width = long - green_width
        if(box.isBoxRented(self.conn, yearmonth)==False):
            self.canvas.create_rectangle(x, y, x + long, y + larg, outline="#DAA520", fill="#DAA520", width=2)
        else:
            if green_width > 0:
                self.canvas.create_rectangle(x, y, x + green_width, y + larg, outline="#4A8", fill="#4A8", width=2)
            if red_width > 0:
                self.canvas.create_rectangle(x + green_width, y, x + long, y + larg, outline="#D9534F", fill="#D9534F", width=2)
        self.canvas.create_text(x + long / 2, y + larg / 2, text=f"Box ID: {box.get_idbox()}", fill="black", font=("Helvetica", 8, "bold"))

    def process_payment(self):
        idbox = self.box_var.get()
        datepaiement = self.date_var.get()
        montant = self.amount_var.get()
        box = Box.getBoxById(self.conn, idbox)
        if box:
            try:
                montant = float(montant)
                box.insertPaiement(self.conn, datepaiement, montant)
                messagebox.showinfo("Success", "Payment processed successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error processing payment: {str(e)}")
        else:
            messagebox.showerror("Error", "Box not found.")

    def open_web_app(self):
        def start_flask_app():
            from waitress import serve
            from web.wsgi import app
            serve(app, host='127.0.0.1', port=5000)
        flask_thread = threading.Thread(target=start_flask_app)
        flask_thread.daemon = True
        flask_thread.start()
        webbrowser.open('http://127.0.0.1:5000')

    def close_connection(self):
        if self.conn:
            self.conn.close()
        self.root.destroy()
