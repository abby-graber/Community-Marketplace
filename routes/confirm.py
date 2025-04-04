from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from notifications.scheduler import schedule_email

# Create a Blueprint for the date-time routes
confirm_bp = Blueprint('confirm', __name__, template_folder="../templates")

mysql = MySQL()

@confirm_bp.route('/confirm', methods=["GET", "POST"])
def confirm_meeting():
    address = session.get('address')
    date = session.get('date')
    time = session.get('time')

    if request.method == 'POST':
        if 'confirm' in request.form:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO meetings (address, date, time) VALUES (%s, %s, %s)",
                (address, date, time)
            )
            mysql.connection.commit()
            cursor.close()
            flash(f'Meeting Scheduled:{time} {date} at {address}', 'success')
            return redirect(url_for('home'))
        elif 'edit' in request.form:
            return redirect(url_for('address.address_page')) # redirect to address

    # Render the form template for GET requests
    return render_template('confirm.html', address=address, date=date, time=time)
