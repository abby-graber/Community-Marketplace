from flask import Blueprint, request, jsonify
from config import mysql 

reviews_bp = Blueprint('reviews', __name__)

# Get all reviews
@reviews_bp.route('/', methods=['GET'])
def get_reviews():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, seller_id, customer_id, rating, review_text FROM reviews")
        reviews = cursor.fetchall()
        cursor.close()

        review_list = [{'id': r[0], 'seller_id': r[1], 'customer_id': r[2], 'rating': r[3], 'review_text': r[4]} for r in reviews]
        return jsonify({'reviews': review_list})
    except Exception as e:
        return jsonify({'error': str(e)})

# Add a new review
@reviews_bp.route('/', methods=['POST'])
def add_review():
    try:
        data = request.get_json()
        seller_id = data.get('seller_id')
        customer_id = data.get('customer_id')
        rating = data.get('rating')
        review_text = data.get('review_text')

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO reviews (seller_id, customer_id, rating, review_text) VALUES (%s, %s, %s, %s)",
                       (seller_id, customer_id, rating, review_text))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Review added successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Update a review
@reviews_bp.route('/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    try:
        data = request.get_json()
        rating = data.get('rating')
        review_text = data.get('review_text')

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE reviews SET rating = %s, review_text = %s WHERE id = %s", (rating, review_text, review_id))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': f'Review ID {review_id} updated successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Delete a review
@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM reviews WHERE id = %s", (review_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': f'Review ID {review_id} deleted successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})




