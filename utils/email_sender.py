import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


#https://myaccount.google.com/apppasswords
SMTP_SERVER = "smtp.gmail.com"  # Change as needed
SMTP_PORT = 587
EMAIL_SENDER = "rosisneupane1@gmail.com"
EMAIL_PASSWORD = "vewn acdn ultr pkwe"

def send_verification_email(recipient_email: str, token: str):
    print("Sending email")
    subject = "Verify Your Email"
    body = f"Your verification token is : {token}"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipient_email, msg.as_string())
        server.quit()
        print(f"Verification email sent to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {e}")



