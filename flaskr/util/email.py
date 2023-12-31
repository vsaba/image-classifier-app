from flask_mail import Message
from flaskr import mail
from flask import url_for, render_template, current_app


def compose_email(verification_token, url, template_path):
    """
    Creates the necessary attributes for creating a Message instance

    :param verification_token: The created verification token
    :param url: The url for verification
    :param template_path: The html template path for the email body
    :return: The html for the email body
    """
    confirm_url = url_for(url, verification_token=verification_token, _external=True)
    html = render_template(template_path, confirm_url=confirm_url)

    return html


def send_email(recipient, subject, body):
    """
    Creates a Message instance from the provided arguments and sends the message via email

    :param recipient: The recipient of the email
    :param subject: The subject of the email
    :param body: The body of the email message
    """
    msg = Message(recipients=[recipient],
                  subject=subject,
                  html=body,
                  sender=current_app.config['DEFAULT_APPLICATION_SENDER_EMAIL'])
    mail.send(msg)
