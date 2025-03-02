from flask import Flask, render_template
from flask_mysqldb import MySQL
from routers.listing import listings_bp
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rootroot'
app.config['MYSQL_DB'] = 'community_marketplace'

mysql = MySQL(app)

app.register_blueprint(listings_bp, url_prefix='/api')
listings_bp.upload_folder = app.config['UPLOAD_FOLDER']

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5500)


