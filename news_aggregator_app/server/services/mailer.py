import smtplib
from email.mime.text import MIMEText
from server.config import Config

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = Config.MAIL_USERNAME
    msg["To"] = to_email

    with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
        server.starttls()
        server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
        server.sendmail(Config.MAIL_USERNAME, [to_email], msg.as_string())