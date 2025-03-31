from flask import Blueprint, request, jsonify, render_template # type: ignore
import requests # type: ignore

# Create a Blueprint for address routes
address_bp = Blueprint("address", __name__, template_folder="../templates")

@address_bp.route("/", methods=["GET"])
def address_page():
    return render_template("address.html")

@address_bp.route("/search_address", methods=["GET"])
def search_address():
    """Get address suggestions from OpenStreetMap"""
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "addressdetails": 1,
        "limit": 5
    }
    headers = {"User-Agent": "YourAppName/1.0"}
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        results = response.json()
    
        if not results:
            return jsonify({"error": "Invalid or unknown location. Please try again."}), 404
        
        return jsonify(results)
    
    return jsonify({"error": "Failed to fetch data"}), 500

