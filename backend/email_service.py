"""
Email service for sending newsletter confirmation and other emails.
Uses SMTP configuration from environment variables.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via SMTP"""
    
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.smtp_from_name = os.getenv("SMTP_FROM_NAME", "Hackathon Hub")
        self.smtp_from_email = os.getenv("SMTP_FROM_EMAIL", "")
        self.use_tls = os.getenv("SMTP_TLS", "true").lower() == "true"
        self.use_ssl = os.getenv("SMTP_SSL", "false").lower() == "true"
        
        # Newsletter templates
        self.welcome_subject = os.getenv(
            "NEWSLETTER_WELCOME_SUBJECT",
            "Welcome to Hackathon Hub Newsletter!"
        )
        self.welcome_body = os.getenv(
            "NEWSLETTER_WELCOME_BODY",
            "Thank you for subscribing to our newsletter. "
            "You'll receive updates about new hackathons, "
            "projects, and community events."
        )
    
    def _create_message(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> MIMEMultipart:
        """Create an email message"""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{self.smtp_from_name} <{self.smtp_from_email}>"
        msg['To'] = to_email
        
        # Add plain text version
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Add HTML version if provided
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
        
        return msg
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> bool:
        """Send an email via SMTP"""
        
        # Check if SMTP is configured
        if not self.smtp_user or not self.smtp_password:
            logger.warning(
                "SMTP not configured. Email would be sent to: %s", to_email
            )
            logger.warning("Subject: %s", subject)
            logger.warning("Body: %s", body[:100] + "..." if len(body) > 100 else body)
            return True  # Return success in development
        
        try:
            # Create message
            msg = self._create_message(to_email, subject, body, html_body)
            
            # Connect to SMTP server
            if self.use_ssl:
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            
            if self.use_tls and not self.use_ssl:
                server.starttls()
            
            # Login and send
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            logger.info("Email sent successfully to: %s", to_email)
            return True
            
        except Exception as e:
            logger.error("Failed to send email to %s: %s", to_email, str(e))
            return False
    
    def send_newsletter_welcome(self, to_email: str) -> bool:
        """Send welcome email to new newsletter subscribers"""
        
        # Create HTML version of welcome email
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4f46e5; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background-color: #f9fafb; padding: 30px; border-radius: 0 0 8px 8px; }}
                .footer {{ text-align: center; margin-top: 30px; color: #6b7280; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to Hackathon Hub!</h1>
                </div>
                <div class="content">
                    <p>Hello,</p>
                    <p>Thank you for subscribing to the Hackathon Hub newsletter. 
                    We're excited to have you as part of our community!</p>
                    <p>You'll receive updates about:</p>
                    <ul>
                        <li>New hackathon announcements</li>
                        <li>Featured projects and success stories</li>
                        <li>Community events and workshops</li>
                        <li>Tips and resources for hackathon participants</li>
                    </ul>
                    <p>If you have any questions or suggestions, feel free to reply to this email.</p>
                    <p>Best regards,<br>The Hackathon Hub Team</p>
                </div>
                <div class="footer">
                    <p>© 2024 Hackathon Hub. All rights reserved.</p>
                    <p><a href="[UNSUBSCRIBE_URL]" style="color: #6b7280;">Unsubscribe</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(
            to_email=to_email,
            subject=self.welcome_subject,
            body=self.welcome_body,
            html_body=html_body
        )


# Global email service instance
email_service = EmailService()