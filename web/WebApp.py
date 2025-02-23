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
            message = request.args.get('message', '')
            message_type = request.args.get('message_type', '')
            return render_template('paiement.html', boxes=boxes, message=message, message_type=message_type)

        @self.app.route('/process_payment', methods=['POST'])
        def process_payment():
            idbox = request.form['idbox']
            datepaiement = request.form['datepaiement']
            montant = request.form['montant']
            print(idbox, datepaiement, montant)
            box = Box.getBoxById(idbox)
            if box:
                try:
                    montant = float(montant)
                    box.insertPaiement(datepaiement, montant)
                    message = 'Payment processed successfully.'
                    message_type = 'success'
                except Exception as e:
                    message = f'Error processing payment: {str(e)}'
                    message_type = 'error'
            else:
                message = 'Box not found.'
                message_type = 'error'
            return redirect(url_for('payment', message=message, message_type=message_type))

    def run(self, host='127.0.0.1', port=5000):
        self.app.run(debug=False, host=host, port=port)