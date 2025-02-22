import datetime
from flask import Flask, redirect, render_template, request, url_for
import os
from material.Box import Box
from tool import Paiement

class WebApp:
    def __init__(self):
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
        self.app = Flask(__name__, template_folder=template_dir)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def payment():
            boxes = Box.getBoxs()
            return render_template('paiement.html', boxes=boxes)

        @self.app.route('/process_payment', methods=['POST'])
        def process_payment():
            idbox = request.form['idbox']
            datepaiement = request.form['datepaiement']
            montant = request.form['montant']
            print(idbox, datepaiement, montant)
            box = Box.getBoxById(idbox)
            if box:
                montant = float(montant)
                box.insertPaiement(datepaiement, montant)
            return redirect(url_for('payment'))
            

    def run(self, host='127.0.0.1', port=5000):
        self.app.run(debug=False, host=host, port=port)