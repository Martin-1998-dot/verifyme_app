import smtplib
from email.mime.text import MIMEText

def send_email_alert(to_email, subject, message):
    from_email = "your_email@gmail.com"         # <-- Change this to your Gmail
    from_password = "your_app_password"         # <-- Use Gmail App Password (not normal password)

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(from_email, from_password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False
