from flask import Flask, render_template
import os

class WebApp:
    def __init__(self):
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
        self.app = Flask(__name__, template_folder=template_dir)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def home():
            return render_template('index.html')

    def run(self, host='127.0.0.1', port=5000):
        self.app.run(debug=False, host=host, port=port)