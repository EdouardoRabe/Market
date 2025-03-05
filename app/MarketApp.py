import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from connexion import ConnexionAccess
from dateutil.relativedelta import relativedelta
from material import Market, Box
from tool import Location, Owner
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
        self.yearmonth = tk.StringVar(value="2024-01")
        self.yearmonth.trace("w", self.update_title)
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)
        self.menu_bar.add_command(label="Home", command=self.show_home)
        self.menu_bar.add_command(label="Paiement sur Tkinter", command=self.show_payments)
        self.menu_bar.add_command(label="Paiement sur web", command=self.open_web_app)
        self.menu_bar.add_command(label="Insérer Market", command=self.show_insert_market)
        self.menu_bar.add_command(label="Insérer Box", command=self.show_insert_box)
        self.home_frame = tk.Frame(root, bg="#F0F8FF")
        self.payment_frame = tk.Frame(root, bg="#F0F8FF")
        self.insert_market_frame = tk.Frame(root, bg="#F0F8FF")
        self.insert_box_frame = tk.Frame(root, bg="#F0F8FF")
        self.init_home_page()
        self.init_payment_page()
        self.init_insert_market_page()
        self.init_insert_box_page()
        self.show_home()

        # Bind the close event to the close_connection method
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
        
        self.owner_label = ttk.Label(self.payment_frame, text="Propriétaire:")
        self.owner_label.pack(pady=5)
        self.owner_var = tk.StringVar()
        self.owner_select = ttk.Combobox(self.payment_frame, textvariable=self.owner_var)
        owners = Owner.getOwners(self.conn)
        self.owner_select['values'] = [f"{owner.get_name()} {owner.get_firstname()}" for owner in owners]
        self.owner_select.pack(pady=5)
        
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

    def init_insert_market_page(self):
        self.insert_market_label = ttk.Label(self.insert_market_frame, text="Insérer un marché", font=("Arial", 16, "bold"))
        self.insert_market_label.pack(pady=5)
        
        self.market_long_label = ttk.Label(self.insert_market_frame, text="Longueur:")
        self.market_long_label.pack(pady=5)
        self.market_long_var = tk.StringVar()
        self.market_long_entry = ttk.Entry(self.insert_market_frame, textvariable=self.market_long_var)
        self.market_long_entry.pack(pady=5)
        
        self.market_larg_label = ttk.Label(self.insert_market_frame, text="Largeur:")
        self.market_larg_label.pack(pady=5)
        self.market_larg_var = tk.StringVar()
        self.market_larg_entry = ttk.Entry(self.insert_market_frame, textvariable=self.market_larg_var)
        self.market_larg_entry.pack(pady=5)
        
        self.market_x_label = ttk.Label(self.insert_market_frame, text="X:")
        self.market_x_label.pack(pady=5)
        self.market_x_var = tk.StringVar()
        self.market_x_entry = ttk.Entry(self.insert_market_frame, textvariable=self.market_x_var)
        self.market_x_entry.pack(pady=5)
        
        self.market_y_label = ttk.Label(self.insert_market_frame, text="Y:")
        self.market_y_label.pack(pady=5)
        self.market_y_var = tk.StringVar()
        self.market_y_entry = ttk.Entry(self.insert_market_frame, textvariable=self.market_y_var)
        self.market_y_entry.pack(pady=5)
        
        self.market_nommarket_label = ttk.Label(self.insert_market_frame, text="Nom market:")
        self.market_nommarket_label.pack(pady=5)
        self.market_nommarket_var = tk.StringVar()
        self.market_nommarket_entry = ttk.Entry(self.insert_market_frame, textvariable=self.market_nommarket_var)
        self.market_nommarket_entry.pack(pady=5)
        self.insert_market_button = ttk.Button(self.insert_market_frame, text="Insérer Market", command=self.insert_market)
        self.insert_market_button.pack(pady=5)

    def init_insert_box_page(self):
        self.insert_box_label = ttk.Label(self.insert_box_frame, text="Insérer un box", font=("Arial", 16, "bold"))
        self.insert_box_label.pack(pady=5)
        
        self.idmarket_label = ttk.Label(self.insert_box_frame, text="ID Market:")
        self.idmarket_label.pack(pady=5)
        self.idmarket_var = tk.StringVar()
        self.idmarket_select = ttk.Combobox(self.insert_box_frame, textvariable=self.idmarket_var)
        self.idmarket_select['values'] = [market.get_idmarket() for market in Market.getMarkets(self.conn)]
        self.idmarket_select.pack(pady=5)
        
        self.box_num_label = ttk.Label(self.insert_box_frame, text="Numéro:")
        self.box_num_label.pack(pady=5)
        self.box_num_var = tk.StringVar()
        self.box_num_entry = ttk.Entry(self.insert_box_frame, textvariable=self.box_num_var)
        self.box_num_entry.pack(pady=5)
        
        self.box_long_label = ttk.Label(self.insert_box_frame, text="Longueur:")
        self.box_long_label.pack(pady=5)
        self.box_long_var = tk.StringVar()
        self.box_long_entry = ttk.Entry(self.insert_box_frame, textvariable=self.box_long_var)
        self.box_long_entry.pack(pady=5)
        
        self.box_larg_label = ttk.Label(self.insert_box_frame, text="Largeur:")
        self.box_larg_label.pack(pady=5)
        self.box_larg_var = tk.StringVar()
        self.box_larg_entry = ttk.Entry(self.insert_box_frame, textvariable=self.box_larg_var)
        self.box_larg_entry.pack(pady=5)
        
        self.box_x_label = ttk.Label(self.insert_box_frame, text="X:")
        self.box_x_label.pack(pady=5)
        self.box_x_var = tk.StringVar()
        self.box_x_entry = ttk.Entry(self.insert_box_frame, textvariable=self.box_x_var)
        self.box_x_entry.pack(pady=5)
        
        self.box_y_label = ttk.Label(self.insert_box_frame, text="Y:")
        self.box_y_label.pack(pady=5)
        self.box_y_var = tk.StringVar()
        self.box_y_entry = ttk.Entry(self.insert_box_frame, textvariable=self.box_y_var)
        self.box_y_entry.pack(pady=5)
        self.insert_box_button = ttk.Button(self.insert_box_frame, text="Insérer Box", command=self.insert_box)
        self.insert_box_button.pack(pady=5)

    def show_home(self):
        self.payment_frame.pack_forget()
        self.insert_market_frame.pack_forget()
        self.insert_box_frame.pack_forget()
        self.home_frame.pack(fill=tk.BOTH, expand=True)

    def show_payments(self):
        self.home_frame.pack_forget()
        self.insert_market_frame.pack_forget()
        self.insert_box_frame.pack_forget()
        self.payment_frame.pack(fill=tk.BOTH, expand=True)

    def show_insert_market(self):
        self.home_frame.pack_forget()
        self.payment_frame.pack_forget()
        self.insert_box_frame.pack_forget()
        self.insert_market_frame.pack(fill=tk.BOTH, expand=True)

    def show_insert_box(self):
        self.home_frame.pack_forget()
        self.payment_frame.pack_forget()
        self.insert_market_frame.pack_forget()
        self.insert_box_frame.pack(fill=tk.BOTH, expand=True)

    def update_title(self, *args):
        date_value = self.yearmonth.get()
        self.title_label.config(text=f"Situation de Marché au mois de {date_value}")

    def validate_date(self):
        self.canvas.delete("all")
        self.displayMarkets()

    def displayMarkets(self):
        self.display_legends()
        for market in self.markets:
            self.displayMarket(market)

    def display_legends(self):
        legend_x = 10
        legend_y = 10
        legend_spacing = 200
        self.canvas.create_rectangle(legend_x, legend_y, legend_x + 20, legend_y + 20, outline="#D9534F", fill="#D9534F", width=2)
        self.canvas.create_text(legend_x + 30, legend_y + 10, text="Pourcentage non payé", anchor="w", font=("Helvetica", 10))
        self.canvas.create_rectangle(legend_x + legend_spacing, legend_y, legend_x + legend_spacing + 20, legend_y + 20, outline="#4A8", fill="#4A8", width=2)
        self.canvas.create_text(legend_x + legend_spacing + 30, legend_y + 10, text="Pourcentage payé", anchor="w", font=("Helvetica", 10))
        self.canvas.create_rectangle(legend_x + 2 * legend_spacing, legend_y, legend_x + 2 * legend_spacing + 20, legend_y + 20, outline="#DAA520", fill="#DAA520", width=2)
        self.canvas.create_text(legend_x + 2 * legend_spacing + 30, legend_y + 10, text="Non loué", anchor="w", font=("Helvetica", 10))

    def displayMarket(self, market):
        x, y = market.get_x()*50, market.get_y()*50
        longueur, largeur = market.get_longueur()*50, market.get_largeur()*50
        self.canvas.create_rectangle(x, y, x + longueur, y + largeur, outline="#5A9", width=2)
        self.canvas.create_text(x + longueur / 2, y - 10, text=f"{market.get_nommarket()}", fill="#5A9", font=("Helvetica", 10, "bold"))
        boxes = market.getBoxs(self.conn)
        for box in boxes:
            self.displayBox(box)

    def displayBox(self, box):
        x, y = box.get_x()*50, box.get_y()*50
        longueur, largeur = box.get_longueur()*50, box.get_largeur()*50
        yearmonth = self.yearmonth.get()
        percent_paid = box.getPourcent(self.conn, yearmonth)
        green_width = int(longueur * percent_paid)
        red_width = longueur - green_width
        if(box.isBoxRented(self.conn, yearmonth)==False):
            self.canvas.create_rectangle(x, y, x + longueur, y + largeur, outline="#DAA520", fill="#DAA520", width=2)
        else:
            if green_width > 0:
                self.canvas.create_rectangle(x, y, x + green_width, y + largeur, outline="#4A8", fill="#4A8", width=2)
            if red_width > 0:
                self.canvas.create_rectangle(x + green_width, y, x + longueur, y + largeur, outline="#D9534F", fill="#D9534F", width=2)
        self.canvas.create_text(x + longueur / 2, y + largeur / 2, text=f"Box ID: {box.get_idbox()}", fill="black", font=("Helvetica", 8, "bold"))

    def process_payment(self):
        idbox = self.box_var.get()
        owner_name = self.owner_var.get()
        datepaiement = self.date_var.get()
        montant = self.amount_var.get()
        
        box1=None
        location1=None
        try:
            montant = float(montant)
            owner = next(owner for owner in Owner.getOwners(self.conn) if f"{owner.get_name()} {owner.get_firstname()}" == owner_name)
            owner_boxes = Box.getBoxByIdOwner(self.conn, owner.get_idowner())
            owner_locations = Location.getLocationByOwner(self.conn, owner.get_idowner())
            for location in owner_locations:
                if location.get_fin() is not None:
                    current_date = location.get_debut()
                    fin_location = location.get_fin()
                    while current_date <= fin_location:
                        yearmonth = current_date.strftime('%Y-%m')
                        box = Box.getBoxById(self.conn, location.get_idbox())
                        if box:
                            montant = box.insertPaiement(self.conn, datepaiement, montant, yearmonth, fin_location)
                        current_date += relativedelta(months=1)
                if location.get_fin() is None and location.get_idbox()==int(idbox):
                    box1 = Box.getBoxById(self.conn, location.get_idbox())
                    location1 = location
                    
            if box1 is not None and location1 is not None:
                montant = box1.insertPaiement(self.conn, datepaiement, montant, location1.get_debut().strftime('%Y-%m'), location1.get_fin())

            if montant > 0:
                messagebox.showinfo("Success", "Rent already paied")
            else:    
                messagebox.showinfo("Success", "Payment processed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing payment: {str(e)}")
       


    def insert_market(self):
        try:
            longueur = self.market_long_var.get()
            largeur = self.market_larg_var.get()
            x = self.market_x_var.get()
            y = self.market_y_var.get()
            nommarket = self.market_nommarket_var.get()
            
            if not longueur or not largeur or not x or not y or not nommarket:
                raise ValueError("All fields are required.")
            longueur = float(longueur)
            largeur = float(largeur)
            x = float(x)
            y = float(y)
            Market.insertMarket(self.conn, longueur, largeur, x, y, nommarket)
            messagebox.showinfo("Success", "Market inserted successfully.")
        except ValueError as ve:
            messagebox.showerror("Error", f"Please enter valid numeric values for longueur, largeur, x, and y. {str(ve)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting market: {str(e)}")

    def insert_box(self):
        try:
            idmarket = self.idmarket_var.get()
            num = self.box_num_var.get()
            longueur = self.box_long_var.get()
            largeur = self.box_larg_var.get()
            x = self.box_x_var.get()
            y = self.box_y_var.get()
            if not idmarket or not num or not longueur or not largeur or not x or not y:
                raise ValueError("All fields are required.")
            idmarket = int(idmarket)
            num = int(num)
            longueur = float(longueur)
            largeur = float(largeur)
            x = float(x)
            y = float(y)
            Box.insertBox(self.conn, idmarket, num, longueur, largeur, x, y)
            messagebox.showinfo("Success", "Box inserted successfully.")
        except ValueError as ve:
            messagebox.showerror("Error", f"Please enter valid numeric values for idmarket, num, longueur, largeur, x, and y. {str(ve)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting box: {str(e)}")

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
