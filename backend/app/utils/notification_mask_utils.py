"""
Central BigInt bitmask helpers for notification settings.
"""
from __future__ import annotations

from typing import Iterable


def has_flag(mask: int, flag: int) -> bool:
    return (int(mask) & int(flag)) == int(flag)


def enable_flag(mask: int, flag: int) -> int:
    return int(mask) | int(flag)


def disable_flag(mask: int, flag: int) -> int:
    return int(mask) & ~int(flag)


def toggle_flag(mask: int, flag: int) -> int:
    return int(mask) ^ int(flag)


def enable_all_flags(flags: Iterable[int]) -> int:
    mask = 0
    for flag in flags:
        mask |= int(flag)
    return mask


def are_all_flags_enabled(mask: int, flags: Iterable[int]) -> bool:
    normalized_flags = [int(flag) for flag in flags]
    if not normalized_flags:
        return True
    return all(has_flag(mask, flag) for flag in normalized_flags)


def is_any_flag_enabled(mask: int, flags: Iterable[int]) -> bool:
    return any(has_flag(mask, int(flag)) for flag in flags)
