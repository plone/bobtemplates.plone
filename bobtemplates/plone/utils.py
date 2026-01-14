from bobtemplates.plone.base import _get_package_root_folder

import re
import six
import subprocess
import unicodedata
from lxml import etree
from bobtemplates.plone.base import update_file


def safe_unicode(value, encoding="utf-8"):
    """Converts a value to unicode, even it is already a unicode string."""

    if isinstance(value, str):
        return value
    elif isinstance(value, bytes):
        try:
            value = str(value, encoding)
        except UnicodeDecodeError:
            value = value.decode("utf-8", "replace")
    return value


def safe_encode(value, encoding="utf-8"):
    """Convert unicode to the specified encoding."""
    if isinstance(value, six.text_type):
        value = value.encode(encoding)
    return value


def safe_nativestring(value, encoding="utf-8"):
    """Convert a value to text in py3"""
    if isinstance(value, six.binary_type):
        value = safe_unicode(value, encoding)
    return value


def slugify(value):
    """
    Convert to ASCII and Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = safe_unicode(value)
    value = (
        unicodedata.normalize(
            "NFKD",
            value,
        )
        .encode(
            "ascii",
            "ignore",
        )
        .decode(
            "ascii",
        )
    )
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)
