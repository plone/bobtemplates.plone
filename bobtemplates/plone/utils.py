# -*- coding: utf-8 -*-
from bobtemplates.plone.base import _get_package_root_folder

import re
import six
import subprocess
import unicodedata


def safe_unicode(value, encoding="utf-8"):
    """Converts a value to unicode, even it is already a unicode string."""
    if six.PY2:
        if isinstance(value, unicode):
            return value
        elif isinstance(value, basestring):
            try:
                value = unicode(value, encoding)
            except (UnicodeDecodeError):
                value = value.decode("utf-8", "replace")
        return value

    if isinstance(value, str):
        return value
    elif isinstance(value, bytes):
        try:
            value = str(value, encoding)
        except (UnicodeDecodeError):
            value = value.decode("utf-8", "replace")
    return value


def safe_encode(value, encoding="utf-8"):
    """Convert unicode to the specified encoding."""
    if isinstance(value, six.text_type):
        value = value.encode(encoding)
    return value


def safe_nativestring(value, encoding="utf-8"):
    """Convert a value to str in py2 and to text in py3"""
    if six.PY2 and isinstance(value, six.text_type):
        value = safe_encode(value, encoding)
    if not six.PY2 and isinstance(value, six.binary_type):
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


def run_isort(configurator):
    root_folder = _get_package_root_folder(configurator)
    try:
        test_result = subprocess.check_output(
            ["tox", "-e", "isort-apply"],
            cwd=root_folder,
        )
        print("\nisort-apply: successful:\n{0}\n".format(safe_unicode(test_result)))
    except OSError as e:
        print(
            "Error on isort-apply: {0}, make sure you have tox and isort installed globally!".format(
                safe_unicode(e)
            )
        )
        raise
    except subprocess.CalledProcessError as execinfo:
        print("Error on isort-apply: {0}".format(safe_unicode(execinfo.output)))


def run_black(configurator):
    root_folder = _get_package_root_folder(configurator)
    try:
        test_result = subprocess.check_output(
            ["tox", "-e", "black-enforce"],
            cwd=root_folder,
        )
        print("\nblack-enforce: successful:\n{0}\n".format(safe_unicode(test_result)))
    except OSError as e:
        print(
            "Error on black-enforce: {0}, make sure you have tox an black installed globally!".format(
                safe_unicode(e)
            )
        )
        raise
    except subprocess.CalledProcessError as execinfo:
        print("Error on black-enforce: {0}".format(safe_unicode(execinfo.output)))
