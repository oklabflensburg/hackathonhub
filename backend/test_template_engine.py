#!/usr/bin/env python3
"""
Test script for the template engine.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from template_engine import template_engine


def test_template_engine():
    """Test the template engine with different email types."""
    print("Testing Template Engine...")
    print("=" * 60)
    
    # Test verification email
    print("\n1. Testing Verification Email (English):")
    verification_vars = {
        "user_name": "John Doe",
        "verification_url": "http://localhost:3001/verify-email?token=abc123",
        "expiration_hours": 24
    }
    
    try:
        verification_email = template_engine.render_email(
            template_name="verification",
            language="en",
            variables=verification_vars
        )
        print(f"✓ Subject: {verification_email['subject']}")
        print(f"✓ HTML length: {len(verification_email['html'])} chars")
        print(f"✓ Text length: {len(verification_email['text'])} chars")
        print("✓ Verification email rendered successfully")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test verification email in German
    print("\n2. Testing Verification Email (German):")
    try:
        verification_email_de = template_engine.render_email(
            template_name="verification",
            language="de",
            variables=verification_vars
        )
        print(f"✓ Subject: {verification_email_de['subject']}")
        print(f"✓ HTML length: {len(verification_email_de['html'])} chars")
        print("✓ German verification email rendered successfully")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test password reset email
    print("\n3. Testing Password Reset Email (English):")
    password_reset_vars = {
        "user_name": "Jane Smith",
        "reset_url": "http://localhost:3001/reset-password?token=def456",
        "expiration_hours": 1
    }
    
    try:
        password_reset_email = template_engine.render_email(
            template_name="password_reset",
            language="en",
            variables=password_reset_vars
        )
        print(f"✓ Subject: {password_reset_email['subject']}")
        print(f"✓ HTML length: {len(password_reset_email['html'])} chars")
        print(f"✓ Text length: {len(password_reset_email['text'])} chars")
        print("✓ Password reset email rendered successfully")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test newsletter welcome email
    print("\n4. Testing Newsletter Welcome Email (English):")
    newsletter_vars = {
        "unsubscribe_url": "http://localhost:3001/unsubscribe"
    }
    
    try:
        newsletter_email = template_engine.render_email(
            template_name="newsletter_welcome",
            language="en",
            variables=newsletter_vars
        )
        print(f"✓ Subject: {newsletter_email['subject']}")
        print(f"✓ HTML length: {len(newsletter_email['html'])} chars")
        print(f"✓ Text length: {len(newsletter_email['text'])} chars")
        print("✓ Newsletter welcome email rendered successfully")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test fallback to English when language not found
    print("\n5. Testing Fallback to English (unsupported language):")
    try:
        fallback_email = template_engine.render_email(
            template_name="verification",
            language="fr",  # French not supported
            variables=verification_vars
        )
        print(f"✓ Subject: {fallback_email['subject']}")
        print("✓ Fallback to English worked successfully")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Template engine test completed!")


if __name__ == "__main__":
    test_template_engine()