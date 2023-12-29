from flask_mail import Message
from flaskr import mail


def send_email(recipient, subject, body):
    """
    Composes an email Message from the provided arguments and sends the message via email

    :param recipient: The recipient of the email
    :param subject: The subject of the email
    :param body: The body of the email message
    """
    msg = Message(recipients=[recipient],
                  subject=subject,
                  html=body,
                  sender="interviewapplication98@gmail.com")
    mail.send(msg)
