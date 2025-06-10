from bobtemplates.plone.base import _get_package_root_folder

import re
import six
import subprocess
import unicodedata


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


def run_isort(configurator):
    root_folder = _get_package_root_folder(configurator)
    try:
        test_result = subprocess.check_output(
            ["tox", "-e", "isort-apply"],
            cwd=root_folder,
        )
        print(f"\nisort-apply: successful:\n{safe_unicode(test_result)}\n")
    except OSError as e:
        print(
            f"Error on isort-apply: {safe_unicode(e)},"
            f" make sure you have tox and isort installed globally!"
        )
        raise
    except subprocess.CalledProcessError as execinfo:
        print(f"Error on isort-apply: {safe_unicode(execinfo.output)}")


def run_black(configurator):
    root_folder = _get_package_root_folder(configurator)
    try:
        test_result = subprocess.check_output(
            ["tox", "-e", "black-enforce"],
            cwd=root_folder,
        )
        print(f"\nblack-enforce: successful:\n{safe_unicode(test_result)}\n")
    except OSError as e:
        print(
            f"Error on black-enforce: {safe_unicode(e)},"
            f" make sure you have tox and black installed globally!"
        )
        raise
    except subprocess.CalledProcessError as execinfo:
        print(f"Error on black-enforce: {safe_unicode(execinfo.output)}")
