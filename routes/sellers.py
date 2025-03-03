from flask import Blueprint, request, jsonify
from config import mysql  

sellers_bp = Blueprint('sellers', __name__)

# ✅ GET all sellers
@sellers_bp.route('/', methods=['GET'])
def get_sellers():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, name, email, verification_status FROM sellers")
        sellers = cursor.fetchall()
        cursor.close()

        seller_list = [{'id': s[0], 'name': s[1], 'email': s[2], 'verification_status': s[3]} for s in sellers]
        return jsonify({'sellers': seller_list})
    except Exception as e:
        return jsonify({'error': str(e)})

# ✅ ADD new seller via API (POST)
@sellers_bp.route('/', methods=['POST'])
def add_seller():
    try:
        data = request.get_json()

        # Validate input
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({'error': 'Missing required fields: name, email'}), 400

        name = data.get('name')
        email = data.get('email')

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO sellers (name, email, verification_status) VALUES (%s, %s, 'pending')", (name, email))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Seller added successfully!', 'name': name, 'email': email}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
