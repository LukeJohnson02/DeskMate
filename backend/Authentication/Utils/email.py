"""SMTP email helpers used for verification and password reset messages."""

import smtplib
from email.message import EmailMessage

from config import get_required_env, settings


def send_verification_email(to_email: str, token: str):
    """Send an account verification email.

    Args:
        to_email: Recipient email address.
        token: Signed verification token to embed in the backend verification URL.

    The backend URL comes from configuration so local and production deployments
    can generate links pointing at the correct public API host.
    """

    verify_url = f"{settings.backend_public_url}/users/verify-email?token={token}"
    subject = "Please verify your email"
    body = f"Click the link to verify your email: {verify_url}"

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = get_required_env("FROM_EMAIL")
    msg["To"] = to_email

    with smtplib.SMTP(
        get_required_env("SMTP_SERVER"),
        int(get_required_env("SMTP_PORT")),
    ) as server:
        server.starttls()
        server.login(
            get_required_env("SMTP_USERNAME"),
            get_required_env("SMTP_PASSWORD"),
        )
        server.send_message(msg)


def send_reset_email(to_email: str, token: str):
    """Send a password-reset email to a user.

    Args:
        to_email: Recipient email address.
        token: Signed password-reset token.

    The frontend URL is used here because the user should land on a browser page
    that can collect the new password before calling the API.
    """

    reset_url = f"{settings.frontend_public_url}/reset-password?token={token}"
    subject = "Password Reset Request"
    body = f"""
    You requested to reset your password.
    Click the link below to proceed:

    {reset_url}

    If you did not request this, please ignore this email.
    """

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = get_required_env("FROM_EMAIL")
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP(
        get_required_env("SMTP_SERVER"),
        int(get_required_env("SMTP_PORT")),
    ) as smtp:
        smtp.starttls()
        smtp.login(
            get_required_env("SMTP_USERNAME"),
            get_required_env("SMTP_PASSWORD"),
        )
        smtp.send_message(msg)
