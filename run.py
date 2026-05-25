from flask import Flask, render_template
from flask_cors import CORS
from app.models import db
from app.routes.api import api_bp
import os

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    CORS(app)

    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/wordcounter.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def index(): return render_template('seo.html', page='seo')

    @app.route('/geo')
    def geo(): return render_template('geo.html', page='geo')

    @app.route('/aeo')
    def aeo(): return render_template('aeo.html', page='aeo')

    @app.route('/aio')
    def aio(): return render_template('aio.html', page='aio')

    @app.route('/sxo')
    def sxo(): return render_template('sxo.html', page='sxo')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
