# -*- coding: utf-8 -*-
from bobtemplates import hooks
from mrbob.bobexceptions import ValidationError

import pytest


def test_to_boolean():
    # Initial simple test to show coverage in hooks.py.
    assert hooks.to_boolean(None, None, 'y')
    assert hooks.to_boolean(None, None, 'yes')
    assert hooks.to_boolean(None, None, 'true')
    assert hooks.to_boolean(None, None, '1')
    assert hooks.to_boolean(None, None, 'n') is False
    assert hooks.to_boolean(None, None, 'no') is False
    assert hooks.to_boolean(None, None, 'false') is False
    assert hooks.to_boolean(None, None, '0') is False
    with pytest.raises(ValidationError, msg='Value must be a boolean (y/n)'):
        assert hooks.to_boolean(None, None, 'spam')
