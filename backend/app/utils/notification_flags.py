"""
Canonical notification and channel flags.
"""
from __future__ import annotations

from typing import Dict

from app.services.notification_registry import iter_definitions
from app.utils.notification_mask_utils import enable_all_flags


CHANNEL_FLAGS: Dict[str, int] = {
    "email": 1 << 0,
    "push": 1 << 1,
    "in_app": 1 << 2,
}

TYPE_FLAGS: Dict[str, int] = {
    definition.type_key: 1 << index
    for index, definition in enumerate(iter_definitions())
}

ALL_CHANNEL_FLAGS_MASK = enable_all_flags(CHANNEL_FLAGS.values())
ALL_TYPE_FLAGS_MASK = enable_all_flags(TYPE_FLAGS.values())
