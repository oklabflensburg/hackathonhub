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

from template_engine import template_engine

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
    
    def send_newsletter_welcome(
        self,
        to_email: str,
        language: str = "en"
    ) -> bool:
        """Send welcome email to new newsletter subscribers"""
        
        # Prepare template variables
        variables = {
            "unsubscribe_url": "[UNSUBSCRIBE_URL]"  # Should be replaced
        }
        
        # Render email using template engine
        email_content = template_engine.render_email(
            template_name="newsletter_welcome",
            language=language,
            variables=variables
        )
        
        return self.send_email(
            to_email=to_email,
            subject=email_content["subject"],
            body=email_content["text"],
            html_body=email_content["html"]
        )


# Global email service instance
email_service = EmailService()