import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import EMAIL_CONFIG, BASE_DIR

AUTH_LOG = BASE_DIR / "auth_requests.log"

def log_event(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {message}"
    print(formatted)
    try:
        with open(AUTH_LOG, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def send_auth_request_email(platform: str, company: str, role: str, reason: str, action_url: str = "") -> bool:
    """
    Sends an urgent email notification to the user requesting authorization/OTP/2FA/review.
    """
    subject = f"⚠️ [ACTION REQUIRED] Authorization Needed: {company} ({role}) on {platform}"
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #222;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px;">
            <h2 style="color: #0a66c2;">Job Application Bot — Authorization Request</h2>
            <p>Hello Suchir,</p>
            <p>Your automated job application agent requires your authorization to proceed with an application:</p>
            
            <div style="background-color: #f8fafc; padding: 15px; border-left: 4px solid #f59e0b; margin: 15px 0;">
                <p><strong>Platform:</strong> {platform}</p>
                <p><strong>Company:</strong> {company}</p>
                <p><strong>Role:</strong> {role}</p>
                <p><strong>Reason:</strong> <span style="color: #b45309; font-weight: bold;">{reason}</span></p>
                {f'<p><strong>Action URL:</strong> <a href="{action_url}">{action_url}</a></p>' if action_url else ''}
            </div>

            <p>Please log in or approve the prompt in your terminal session/browser window to allow the bot to continue.</p>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 20px 0;">
            <p style="font-size: 0.85em; color: #64748b;">Automated Career Agent &bull; Bengaluru, India</p>
        </div>
    </body>
    </html>
    """

    plain_body = f"""
    JOB APPLICATION BOT — AUTHORIZATION REQUIRED
    -------------------------------------------
    Platform: {platform}
    Company: {company}
    Role: {role}
    Reason: {reason}
    Action URL: {action_url}

    Please approve the prompt in your terminal/browser session to allow the bot to proceed.
    """

    log_event(f"ALERT: Authorization required for {company} on {platform} -> {reason}")
    return _send_email(subject, plain_body, html_body)

def send_submission_email(platform: str, company: str, role: str, application_notes: str = "") -> bool:
    """
    Sends a confirmation email after an application has been successfully submitted.
    """
    subject = f"✅ [APPLICATION SUBMITTED] {company} - {role} ({platform})"
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #222;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px;">
            <h2 style="color: #10b981;">Application Submitted Successfully!</h2>
            <p>Hello Suchir,</p>
            <p>Your automated job application agent has successfully tailored and submitted your application:</p>
            
            <div style="background-color: #f0fdf4; padding: 15px; border-left: 4px solid #10b981; margin: 15px 0;">
                <p><strong>Platform:</strong> {platform}</p>
                <p><strong>Company:</strong> {company}</p>
                <p><strong>Role:</strong> {role}</p>
                <p><strong>Status:</strong> Applied</p>
                <p><strong>Notes:</strong> {application_notes}</p>
            </div>

            <p>The record has been updated in your <a href="file://{BASE_DIR}/dashboard.html">Career Command Center</a>.</p>
        </div>
    </body>
    </html>
    """
    plain_body = f"Application Submitted for {company} ({role}) on {platform}!\nNotes: {application_notes}"
    
    log_event(f"SUCCESS: Submitted application for {company} on {platform}")
    return _send_email(subject, plain_body, html_body)

def _send_email(subject: str, plain_body: str, html_body: str) -> bool:
    sender = EMAIL_CONFIG.get("sender_email")
    password = EMAIL_CONFIG.get("sender_password")
    recipient = EMAIL_CONFIG.get("recipient_email")
    smtp_server = EMAIL_CONFIG.get("smtp_server")
    smtp_port = EMAIL_CONFIG.get("smtp_port")

    if not password:
        log_event(f"ℹ️ [Email Dispatch] SMTP App Password not set in environment. Notification logged to {AUTH_LOG}")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient

        msg.attach(MIMEText(plain_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())

        log_event(f"Email sent successfully to {recipient} with subject: {subject}")
        return True
    except Exception as e:
        log_event(f"Failed to send email: {e}")
        return False

if __name__ == "__main__":
    send_auth_request_email("LinkedIn", "Sarvam AI", "AI/ML Engineer Intern", "2FA Verification Code Prompt", "https://linkedin.com/jobs")
