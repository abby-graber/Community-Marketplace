from flask import Blueprint, request, jsonify
from config import mysql  # Import MySQL from config.py

responses_bp = Blueprint('responses', __name__)

# Get all responses
@responses_bp.route('/', methods=['GET'])
def get_responses():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, review_id, seller_id, response_text FROM responses")
        responses = cursor.fetchall()
        cursor.close()

        response_list = [{'id': r[0], 'review_id': r[1], 'seller_id': r[2], 'response_text': r[3]} for r in responses]
        return jsonify({'responses': response_list})
    except Exception as e:
        return jsonify({'error': str(e)})

# Add a new response
@responses_bp.route('/', methods=['POST'])
def add_response():
    try:
        data = request.get_json()
        review_id = data.get('review_id')
        seller_id = data.get('seller_id')
        response_text = data.get('response_text')

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO responses (review_id, seller_id, response_text) VALUES (%s, %s, %s)",
                       (review_id, seller_id, response_text))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Response added successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Update a response
@responses_bp.route('/<int:response_id>', methods=['PUT'])
def update_response(response_id):
    try:
        data = request.get_json()
        response_text = data.get('response_text')

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE responses SET response_text = %s WHERE id = %s", (response_text, response_id))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': f'Response ID {response_id} updated successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Delete a response
@responses_bp.route('/<int:response_id>', methods=['DELETE'])
def delete_response(response_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM responses WHERE id = %s", (response_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': f'Response ID {response_id} deleted successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})
