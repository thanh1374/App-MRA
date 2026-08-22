"""Filename sanitization utilities."""

from __future__ import annotations

import re
import unicodedata


def sanitize_filename(name: str, max_length: int = 50) -> str:
    """Sanitize a string for use in a filename.

    - Replace spaces with underscores
    - Remove special characters
    - Truncate to max_length
    """
    # Normalize unicode
    name = unicodedata.normalize("NFKD", name)
    # Replace spaces/special chars
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s]+", "_", name)
    name = name.strip("_")
    return name[:max_length].lower()
