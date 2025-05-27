import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class Mail:
    def sending_mail(self, sender, receiver, subject, body):
        app_password = os.getenv("APP_PASSWORD")

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = ",".join(receiver) if isinstance(receiver, list) else receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, app_password)
            server.sendmail(sender, receiver, msg.as_string())
            server.quit()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Email sent to {msg['To']}")
            return "Success"
        except Exception as e:
            print("Failed to send email:", e)
            return "Failed" 