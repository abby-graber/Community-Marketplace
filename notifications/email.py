from flask_mail import Message

def send_email_reminder(to, subject, body):
    from app import mail
    msg = Message(subject, recipients=[to])
    msg.body = body
    mail.send(msg)
