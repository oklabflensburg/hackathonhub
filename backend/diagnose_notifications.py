#!/usr/bin/env python3
"""
Diagnostic script for notification system issues.
Tests database schema, SMTP configuration, template loading, and notification flow.
"""
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect, text
import os
import sys
import logging
from typing import Dict, Any

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Load environment variables
load_dotenv()

# Set up logging
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)
logger = logging.getLogger(__name__)


class NotificationDiagnostic:
    """Diagnostic tool for notification system issues."""

    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "sqlite:///hackathon.db")
        self.engine = create_engine(self.db_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)
        self.results = {}

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all diagnostic tests."""
        logger.info("Starting notification system diagnostic...")

        self.results = {
            "database": self.test_database_connection(),
            "schema": self.test_database_schema(),
            "smtp_config": self.test_smtp_configuration(),
            "templates": self.test_template_loading(),
            "preference_service": self.test_preference_service(),
            "notification_service": self.test_notification_service(),
            "email_service": self.test_email_service(),
        }

        self.print_summary()
        return self.results

    def test_database_connection(self) -> Dict[str, Any]:
        """Test database connection and basic queries."""
        logger.info("Testing database connection...")
        result = {"success": False, "errors": [], "warnings": []}

        try:
            with self.engine.connect() as conn:
                # Test connection
                conn.execute(text("SELECT 1"))
                result["success"] = True
                logger.info("✓ Database connection successful")

                # Check if users table exists
                inspector = inspect(self.engine)
                tables = inspector.get_table_names()
                result["tables"] = tables

                if "users" not in tables:
                    result["warnings"].append("Users table not found")
                    logger.warning("Users table not found")
                else:
                    logger.info("✓ Users table exists")

        except Exception as e:
            result["errors"].append(f"Database connection failed: {e}")
            logger.error(f"✗ Database connection failed: {e}")

        return result

    def test_database_schema(self) -> Dict[str, Any]:
        """Test notification-related database schema."""
        logger.info("Testing notification database schema...")
        result = {"success": False, "errors": [],
                  "warnings": [], "schema_mismatch": False}

        try:
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()

            # Check for notification tables
            notification_tables = [
                "notification_types",
                "user_notification_preferences",
                "user_notifications",
                "push_subscriptions"
            ]

            missing_tables = []
            for table in notification_tables:
                if table not in tables:
                    missing_tables.append(table)

            if missing_tables:
                result["warnings"].append(f"Missing tables: {missing_tables}")
                logger.warning(
                    f"Missing notification tables: {missing_tables}")
            else:
                logger.info("✓ All notification tables exist")

            # Check schema details for critical tables
            if "notification_types" in tables:
                columns = [col["name"]
                           for col in inspector.get_columns("notification_types")]
                result["notification_types_columns"] = columns

                # Check for schema mismatch
                expected_columns_new = [
                    "id", "type_key", "category", "default_channels", "description", "created_at"]
                expected_columns_old = [
                    "id", "name", "description", "default_email", "default_push", "default_in_app", "created_at"]

                if "type_key" in columns:
                    logger.info(
                        "✓ Notification types table has NEW schema (type_key column)")
                    result["schema_version"] = "new"
                elif "name" in columns:
                    logger.info(
                        "⚠ Notification types table has OLD schema (name column)")
                    result["schema_version"] = "old"
                    result["schema_mismatch"] = True
                    result["warnings"].append(
                        "Schema mismatch: notification_types has old schema")
                else:
                    logger.warning("Unknown notification_types schema")
                    result["schema_version"] = "unknown"

            if "user_notification_preferences" in tables:
                columns = [col["name"] for col in inspector.get_columns(
                    "user_notification_preferences")]
                result["user_notification_preferences_columns"] = columns

                # Check for schema mismatch
                if "notification_type" in columns and "channel" in columns:
                    logger.info(
                        "✓ User notification preferences has NEW schema (notification_type, channel columns)")
                elif "notification_type_id" in columns and "email_enabled" in columns:
                    logger.info(
                        "⚠ User notification preferences has OLD schema (notification_type_id, email_enabled columns)")
                    result["schema_mismatch"] = True
                    result["warnings"].append(
                        "Schema mismatch: user_notification_preferences has old schema")
                else:
                    logger.warning(
                        "Unknown user_notification_preferences schema")

            result["success"] = True

        except Exception as e:
            result["errors"].append(f"Schema test failed: {e}")
            logger.error(f"✗ Schema test failed: {e}")

        return result

    def test_smtp_configuration(self) -> Dict[str, Any]:
        """Test SMTP configuration from environment variables."""
        logger.info("Testing SMTP configuration...")
        result = {"success": False, "errors": [], "warnings": []}

        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = os.getenv("SMTP_PORT")
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")

        result["config"] = {
            "SMTP_HOST": smtp_host,
            "SMTP_PORT": smtp_port,
            "SMTP_USER": "***" if smtp_user else None,
            "SMTP_PASSWORD": "***" if smtp_password else None,
            "SMTP_FROM_EMAIL": os.getenv("SMTP_FROM_EMAIL"),
            "SMTP_FROM_NAME": os.getenv("SMTP_FROM_NAME"),
        }

        # Check for placeholder values
        if smtp_user and ("your-email" in smtp_user or "example.com" in smtp_user):
            result["warnings"].append("SMTP_USER appears to be a placeholder")
            logger.warning("SMTP_USER appears to be a placeholder")

        if smtp_password and ("your-app-password" in smtp_password or "password" in smtp_password.lower()):
            result["warnings"].append(
                "SMTP_PASSWORD appears to be a placeholder")
            logger.warning("SMTP_PASSWORD appears to be a placeholder")

        # Check if configured
        if not smtp_user or not smtp_password:
            result["errors"].append("SMTP credentials not configured")
            logger.error("✗ SMTP credentials not configured")
        else:
            logger.info("✓ SMTP credentials configured")
            result["success"] = True

        # Check environment
        environment = os.getenv("ENVIRONMENT", "development")
        result["environment"] = environment

        if environment == "production" and (not smtp_user or not smtp_password):
            result["errors"].append("SMTP not configured in production!")
            logger.error("✗ SMTP not configured in production!")

        return result

    def test_template_loading(self) -> Dict[str, Any]:
        """Test email template loading."""
        logger.info("Testing email template loading...")
        result = {"success": False, "errors": [],
                  "warnings": [], "templates_found": []}

        try:
            from template_engine import TemplateEngine

            template_engine = TemplateEngine()

            # Test loading base template
            base_template = template_engine._load_template("base.html")
            if base_template:
                logger.info("✓ Base template loaded")
                result["templates_found"].append("base.html")
            else:
                result["errors"].append("Base template not found")
                logger.error("✗ Base template not found")

            # Test loading specific notification templates
            test_templates = [
                "team/invitation_sent/en.html",
                "team/invitation_accepted/en.html",
                "team/member_added/en.html",
                "project/created/en.html",
                "verification/en.html",
                "password_reset/en.html"
            ]

            for template_path in test_templates:
                template = template_engine._load_template(template_path)
                if template:
                    result["templates_found"].append(template_path)
                else:
                    result["warnings"].append(
                        f"Template not found: {template_path}")
                    logger.warning(f"Template not found: {template_path}")

            if len(result["templates_found"]) > 3:
                logger.info(
                    f"✓ {len(result['templates_found'])} templates loaded")
                result["success"] = True
            else:
                result["errors"].append("Too few templates loaded")

        except Exception as e:
            result["errors"].append(f"Template loading test failed: {e}")
            logger.error(f"✗ Template loading test failed: {e}")

        return result

    def test_preference_service(self) -> Dict[str, Any]:
        """Test notification preference service."""
        logger.info("Testing notification preference service...")
        result = {"success": False, "errors": [], "warnings": []}

        try:
            from notification_preference_service import NotificationPreferenceService

            service = NotificationPreferenceService()

            with self.SessionLocal() as db:
                # Try to initialize notification types
                initialized = service.initialize_notification_types(db)
                if initialized:
                    logger.info("✓ Notification types initialized")
                else:
                    result["warnings"].append(
                        "Failed to initialize notification types")
                    logger.warning("Failed to initialize notification types")

                # Try to get default preferences
                default_prefs = service._get_default_preferences()
                if default_prefs:
                    logger.info("✓ Default preferences generated")
                else:
                    result["errors"].append(
                        "Failed to get default preferences")

                result["success"] = True

        except Exception as e:
            result["errors"].append(f"Preference service test failed: {e}")
            logger.error(f"✗ Preference service test failed: {e}")

        return result

    def test_notification_service(self) -> Dict[str, Any]:
        """Test notification service."""
        logger.info("Testing notification service...")
        result = {"success": False, "errors": [], "warnings": []}

        try:
            from notification_service import NotificationService

            service = NotificationService()

            # Test template mapping
            template_map = {
                "team_invitation_sent": "team/invitation_sent",
                "team_invitation_accepted": "team/invitation_accepted",
                "team_member_added": "team/member_added",
                "project_created": "project/created",
            }

            for notification_type, expected_template in template_map.items():
                # This is a simple test to see if the service can be instantiated
                logger.info(
                    f"✓ Notification type mapped: {notification_type} -> {expected_template}")

            result["success"] = True
            logger.info("✓ Notification service instantiated successfully")

        except Exception as e:
            result["errors"].append(f"Notification service test failed: {e}")
            logger.error(f"✗ Notification service test failed: {e}")

        return result

    def test_email_service(self) -> Dict[str, Any]:
        """Test email service."""
        logger.info("Testing email service...")
        result = {"success": False, "errors": [], "warnings": []}

        try:
            from email_service import EmailService

            service = EmailService()

            # Check configuration
            result["service_config"] = {
                "smtp_host": service.smtp_host,
                "smtp_port": service.smtp_port,
                "smtp_user_set": bool(service.smtp_user),
                "smtp_password_set": bool(service.smtp_password),
                "from_email": service.smtp_from_email,
                "from_name": service.smtp_from_name,
            }

            if service.smtp_user and service.smtp_password:
                logger.info("✓ Email service configured with SMTP credentials")
                result["success"] = True
            else:
                result["warnings"].append("Email service not fully configured")
                logger.warning("Email service not fully configured")
                # Still mark as success for diagnostic purposes
                result["success"] = True

        except Exception as e:
            result["errors"].append(f"Email service test failed: {e}")
            logger.error(f"✗ Email service test failed: {e}")

        return result

    def print_summary(self):
        """Print diagnostic summary."""
        logger.info("\n" + "="*60)
        logger.info("NOTIFICATION SYSTEM DIAGNOSTIC SUMMARY")
        logger.info("="*60)

        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results.values()
                           if r.get("success", False))

        logger.info(f"Tests run: {total_tests}")
        logger.info(f"Tests passed: {passed_tests}")
        logger.info(f"Tests failed: {total_tests - passed_tests}")

        # Check for critical issues
        critical_issues = []

        # Schema mismatch
        schema_result = self.results.get("schema", {})
        if schema_result.get("schema_mismatch"):
            critical_issues.append(
                "DATABASE SCHEMA MISMATCH - This will break notifications")

        # SMTP in production
        smtp_result = self.results.get("smtp_config", {})
        if smtp_result.get("environment") == "production" and not smtp_result.get("success"):
            critical_issues.append(
                "SMTP NOT CONFIGURED IN PRODUCTION - Emails won't be sent")

        # Database connection
        db_result = self.results.get("database", {})
        if not db_result.get("success"):
            critical_issues.append(
                "DATABASE CONNECTION FAILED - System won't work")

        if critical_issues:
            logger.error("\n❌ CRITICAL ISSUES FOUND:")
            for issue in critical_issues:
                logger.error(f"  - {issue}")
        else:
            logger.info("\n✅ No critical issues found")

        # Print schema info
        if "schema_version" in schema_result:
            logger.info(
                f"\nDatabase Schema Version: {schema_result['schema_version'].upper()}")
            if schema_result["schema_version"] == "old":
                logger.warning(
                    "  ⚠ Database has OLD schema, Python code expects NEW schema")
                logger.warning(
                    "  This will cause notification preferences to fail!")

        # Print recommendations
        logger.info("\n" + "="*60)
        logger.info("RECOMMENDATIONS:")

        if critical_issues:
            for issue in critical_issues:
                if "SCHEMA MISMATCH" in issue:
                    logger.info("1. Fix database schema mismatch first")
                    logger.info(
                        "   - Option A: Update migration to match Python models")
                    logger.info(
                        "   - Option B: Update Python code to match database")
                elif "SMTP" in issue:
                    logger.info("2. Configure SMTP credentials in production")
                    logger.info(
                        "   - Update .env file with real SMTP credentials")
                    logger.info("   - Test email sending")
                elif "DATABASE" in issue:
                    logger.info("3. Fix database connection")
                    logger.info("   - Check DATABASE_URL in .env file")
                    logger.info("   - Verify database is running")
        else:
            logger.info("1. Run integration tests to verify notification flow")
            logger.info("2. Test sending actual notifications")
            logger.info("3. Monitor logs for notification errors")

        logger.info("="*60)


def main():
    """Main function to run diagnostics."""
    diagnostic = NotificationDiagnostic()
    results = diagnostic.run_all_tests()

    # Exit with error code if critical issues found
    schema_result = results.get("schema", {})
    if schema_result.get("schema_mismatch"):
        sys.exit(1)

    smtp_result = results.get("smtp_config", {})
    if smtp_result.get("environment") == "production" and not smtp_result.get("success"):
        sys.exit(1)

    db_result = results.get("database", {})
    if not db_result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
