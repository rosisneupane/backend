import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


#https://myaccount.google.com/apppasswords
SMTP_SERVER = "smtp.gmail.com"  # Change as needed
SMTP_PORT = 587
EMAIL_SENDER = "rosisneupane1@gmail.com"
EMAIL_PASSWORD = "vewn acdn ultr pkwe"

def send_email_to_guardian(recipient_email: str):
    print("Sending email")
    subject = "Emergency Email"
    body = (
        "Dear Guardian,\n\n"
        "This is an emergency alert concerning your child. They may be in distress or require immediate assistance.\n\n"
        "Please try to contact them as soon as possible, or reach out to the relevant authorities or support services if you are unable to do so.\n\n"
        "This message was sent automatically by the safety monitoring system.\n\n"
        "Best regards,\n"
        "Child Safety Monitoring Team"
    )


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
    except Exception as e:
        print(f"Error sending email: {e}")



