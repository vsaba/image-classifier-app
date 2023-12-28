from flask_mail import Message
from flaskr import mail


def send_email(recipient, subject, body):
    msg = Message(recipients=[recipient], subject=subject, html=body, sender="interviewapplication98@gmail.com")
    mail.send(msg)
