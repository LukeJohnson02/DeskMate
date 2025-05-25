import smtplib
from email.message import EmailMessage

SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USERNAME = "your_email@example.com"
SMTP_PASSWORD = "your_email_password"
FROM_EMAIL = SMTP_USERNAME

def send_verification_email(to_email: str, token: str):
    verify_url = f"http://localhost:8000/users/verify-email?token={token}"
    subject = "Please verify your email"
    body = f"Click the link to verify your email: {verify_url}"

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)


def send_reset_email(to_email: str, token: str):
    reset_url = f"http://localhost:3000/reset-password?token={token}"  # Update frontend URL
    subject = "Password Reset Request"
    body = f"""
    You requested to reset your password.
    Click the link below to proceed:

    {reset_url}

    If you did not request this, please ignore this email.
    """

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "noreply@yourdomain.com"
    msg["To"] = to_email
    msg.set_content(body)

    # Send the email (update with your SMTP settings)
    with smtplib.SMTP("smtp.yourprovider.com", 587) as smtp:
        smtp.starttls()
        smtp.login("your_username", "your_password")
        smtp.send_message(msg)