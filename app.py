
from flask import Flask, render_template
from flask_mysqldb import MySQL
from routers.listing import listings_bp
import os
import config

from routes.address import address_bp
from routes.date_time import date_time_bp

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

app.config['MYSQL_HOST'] = config.MYSQL_CONFIG['host']
app.config['MYSQL_USER'] = config.MYSQL_CONFIG['user']
app.config['MYSQL_PASSWORD'] = config.MYSQL_CONFIG['password']
app.config['MYSQL_DB'] = config.MYSQL_CONFIG['database']

app.register_blueprint(address_bp, url_prefix="/address")
app.register_blueprint(date_time_bp, url_prefix="/date-time")

mysql = MySQL(app)

app.register_blueprint(listings_bp, url_prefix='/listings')
listings_bp.upload_folder = app.config['UPLOAD_FOLDER']

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5500)


