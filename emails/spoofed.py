
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class SendSpoofed:
    def __init__(self, sender_email, receiver_email, subject, html_content):
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.subject = subject
        self.html_content = html_content

    def send_email(self):

        message = MIMEMultipart()
        message.attach(MIMEText(self.html_content, "html"))

        message['Subject'] = self.subject
        message['From'] = self.sender_email
        message['To'] = self.receiver_email


        smtp_server= 'ebonyjadehealth.com'
        smtp_port = 587
        smtp_username = 'mail@ebonyjadehealth.com'
        smtp_password = 'bk7bm%v#8VKR!'

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(self.sender_email, self.receiver_email, message.as_string())
            print("Email sent successfully!")
