import smtplib
import datetime
from email.message import EmailMessage


class SendMail:
    def __init__(self, subject, body, sender, recipient):
        self.subject = subject
        self.body = body
        self.sender = sender
        self.recipient = recipient

    def send_message_to_user(self, gmail_user, gmail_password):
        msg = EmailMessage()
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = self.recipient
        msg.set_content(self.body)
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(gmail_user, gmail_password)
            connection.send_message(msg)
