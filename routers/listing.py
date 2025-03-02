from flask import Blueprint, request, jsonify, current_app
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename

listings_bp = Blueprint('listings', __name__)

mysql = MySQL()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@listings_bp.route('/listings', methods=['POST'])
def create_listing():
    seller_id = request.form['seller_id']
    title = request.form['title']
    price = request.form['price']
    category = request.form['category']
    description = request.form['description']
    
    image = request.files['image']
    image_url = None
    
    upload_folder = listings_bp.upload_folder

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(upload_folder, filename))
        image_url = os.path.join('uploads', filename)

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO listings (seller_id, title, price, category, description, image_url) VALUES (%s, %s, %s, %s, %s, %s)",
        (seller_id, title, price, category, description, image_url)
    )
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Listing created successfully'}), 201
