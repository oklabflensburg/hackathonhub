#!/usr/bin/env python3
"""
Validate notification email templates against the template registry.
"""
from __future__ import annotations

import json

from app.utils.template_registry import TemplateRegistry


def main() -> int:
    report = TemplateRegistry.validate_template_files()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
