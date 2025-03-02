from flask import Flask, render_template # type: ignore
from flask_mysqldb import MySQL # type: ignore
import config

# Import blueprints
from routes.address import address_bp
from routes.date_time import date_time_bp

app = Flask(__name__)

app.config['MYSQL_HOST'] = config.MYSQL_CONFIG['host']
app.config['MYSQL_USER'] = config.MYSQL_CONFIG['user']
app.config['MYSQL_PASSWORD'] = config.MYSQL_CONFIG['password']
app.config['MYSQL_DB'] = config.MYSQL_CONFIG['database']

# Register blueprints
app.register_blueprint(address_bp, url_prefix="/address")
app.register_blueprint(date_time_bp, url_prefix="/date-time")

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/users')
def get_users():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        return {'users': users}
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run(debug=True, port=5500)

