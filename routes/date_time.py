from flask import Blueprint, render_template, request # type: ignore

# Create a Blueprint for the date-time routes
date_time_bp = Blueprint('date_time', __name__, template_folder="../templates")

@date_time_bp.route('/set-date-time', methods=["GET", "POST"])
def set_date_time():
    # Get the address from the query parameters
    address = request.args.get('address')

    if request.method == 'POST':
        # Handle form submission (date and time)
        date = request.form.get('date')
        time = request.form.get('time')
        # Process the date and time (e.g., store in the database)
        return f"Date and time set for {address}: {date} at {time}"

    # Render the form template for GET requests
    return render_template('set_date_time.html', address=address)
