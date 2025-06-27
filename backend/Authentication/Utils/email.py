import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()


def send_verification_email(to_email: str, token: str):
    verify_url = f"http://localhost:8000/users/verify-email?token={token}"
    subject = "Please verify your email"
    body = f"Click the link to verify your email: {verify_url}"

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("FROM_EMAIL")
    msg["To"] = to_email

    with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
        server.send_message(msg)


def send_reset_email(to_email: str, token: str):
    reset_url = (
        f"http://localhost:3000/reset-password?token={token}"  # Update frontend URL
    )
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
