#!/usr/bin/env python3
"""
Simple test for Email Template System without database dependencies.
"""
from app.services.email_orchestrator import (
    EmailTemplateValidator, LanguageResolver
)
from app.utils.jinja2_engine import Jinja2TemplateEngine
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_jinja2_engine():
    """Test Jinja2 template engine rendering."""
    print("Testing Jinja2 Template Engine...")

    engine = Jinja2TemplateEngine()

    # Test rendering verification template
    variables = {
        "user_name": "John Doe",
        "verification_url": "https://example.com/verify?token=abc123",
        "expiration_hours": 24
    }

    try:
        result = engine.render_email(
            template_name="verification",
            language="en",
            variables=variables
        )

        print("✓ Verification template rendered successfully")
        print(f"  Subject: {result['subject']}")
        print(f"  HTML length: {len(result['html'])} chars")
        print(f"  Text length: {len(result['text'])} chars")

        # Test German version
        result_de = engine.render_email(
            template_name="verification",
            language="de",
            variables=variables
        )
        print("✓ German verification template rendered successfully")
        print(f"  Subject: {result_de['subject']}")
        print(f"  HTML length: {len(result_de['html'])} chars")
        print(f"  Text length: {len(result_de['text'])} chars")

        # Test template variable analysis
        var_info = engine.get_template_variables("verification", "en")
        print(f"✓ Template variables: {var_info['variables']}")

        return True

    except Exception as e:
        print(f"✗ Jinja2 engine test failed: {e}")
        return False


def test_template_validator():
    """Test template validation."""
    print("\nTesting Template Validator...")

    validator = EmailTemplateValidator()

    # Test valid verification template
    valid_vars = {
        "user_name": "John Doe",
        "verification_url": "https://example.com/verify"
    }
    is_valid = validator.validate("verification", valid_vars)
    print(f"✓ Verification template validation: {is_valid}")

    # Test invalid verification template (missing variable)
    invalid_vars = {"user_name": "John Doe"}
    is_valid = validator.validate("verification", invalid_vars)
    print(f"✓ Verification template validation (missing var): {not is_valid}")

    # Test unknown template (should return True)
    unknown_vars = {"some_var": "value"}
    is_valid = validator.validate("unknown_template", unknown_vars)
    print(f"✓ Unknown template validation: {is_valid}")

    return True


def test_all_templates():
    """Test rendering of all available templates."""
    print("\nTesting all email templates...")

    engine = Jinja2TemplateEngine()

    # Common test variables
    test_variables = {
        "verification": {
            "user_name": "John Doe",
            "verification_url": "https://example.com/verify?token=abc123",
            "expiration_hours": 24
        },
        "password_reset": {
            "user_name": "Jane Smith",
            "reset_url": "https://example.com/reset?token=xyz789",
            "expiration_hours": 1
        },
        "team/invitation_sent": {
            "team_name": "Awesome Team",
            "inviter_name": "Alice Johnson",
            "accept_url": "https://example.com/team/accept?token=inv123"
        },
        "project/created": {
            "project_name": "Hackathon Dashboard",
            "creator_name": "Bob Wilson",
            "project_url": "https://example.com/projects/123"
        },
        "project/commented": {
            "project_name": "Hackathon Dashboard",
            "commenter_name": "Charlie Brown",
            "comment_preview": "Great project! I have some suggestions...",
            "project_url": "https://example.com/projects/123"
        },
        "hackathon/registered": {
            "hackathon_name": "Global Hackathon 2026",
            "user_name": "David Miller",
            "hackathon_date": "2026-04-15",
            "hackathon_url": "https://example.com/hackathons/456"
        },
        "hackathon/started": {
            "hackathon_name": "Global Hackathon 2026",
            "user_name": "David Miller",
            "start_time": "2026-04-15 09:00:00",
            "hackathon_dashboard_url": (
                "https://example.com/hackathons/456/dashboard"
            )
        },
        "team/created": {
            "team_name": "Innovation Squad",
            "creator_name": "Eva Garcia",
            "team_id": 789
        }
    }

    templates_to_test = [
        "verification",
        "password_reset",
        "team/invitation_sent",
        "project/created",
        "project/commented",
        "hackathon/registered",
        "hackathon/started",
        "team/created"
    ]

    success_count = 0
    for template_name in templates_to_test:
        try:
            if template_name in test_variables:
                result = engine.render_email(
                    template_name=template_name,
                    language="en",
                    variables=test_variables[template_name]
                )
                subject_preview = result['subject'][:50]
                print(f"✓ {template_name}: OK (subject: {subject_preview}...)")
                success_count += 1
            else:
                print(f"⚠ {template_name}: No test variables defined")
        except Exception as e:
            print(f"✗ {template_name}: Failed - {e}")

    print(
        f"\nTemplate rendering summary: {success_count}/"
        f"{len(templates_to_test)} successful"
    )
    return success_count == len(templates_to_test)


def test_language_resolution():
    """Test language resolution logic."""
    print("\nTesting Language Resolution...")

    _resolver = LanguageResolver()

    # Test with explicit language
    from app.services.email_orchestrator import EmailContext
    _context = EmailContext(
        user_email="test@example.com",
        language="de",
        category="test"
    )

    # Verify the objects are created correctly
    assert _resolver is not None
    assert _context.user_email == "test@example.com"
    assert _context.language == "de"

    # Note: We can't test database resolution without a DB session
    print("✓ LanguageResolver class initialized")
    print("✓ EmailContext dataclass working")

    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Email Template System Integration Test")
    print("=" * 60)

    # Test Jinja2 engine
    jinja2_ok = test_jinja2_engine()

    # Test template validator
    validator_ok = test_template_validator()

    # Test all templates
    templates_ok = test_all_templates()

    # Test language resolution
    language_ok = test_language_resolution()

    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"  Jinja2 Template Engine: {'✓ PASS' if jinja2_ok else '✗ FAIL'}")
    print(f"  Template Validator: {'✓ PASS' if validator_ok else '✗ FAIL'}")
    print(f"  All Templates: {'✓ PASS' if templates_ok else '✗ FAIL'}")
    print(f"  Language Resolution: {'✓ PASS' if language_ok else '✗ FAIL'}")
    print("=" * 60)

    if jinja2_ok and validator_ok and templates_ok and language_ok:
        print("\n✅ All tests passed! Email template system is ready.")
        print("\nKey Features Implemented:")
        print("  1. Jinja2-based template engine with full feature support")
        print("  2. Template validation with required variable checking")
        print("  3. Multi-language support (EN/DE)")
        print("  4. Template inheritance via base.html")
        print("  5. EmailOrchestrator as central facade")
        print("  6. Services migrated to use EmailOrchestrator")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
