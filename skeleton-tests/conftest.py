# -*- coding: utf-8 -*-

import os
import pytest


class Config(object):
    def __init__(self):
        self.version = None
        self.verbose = None
        self.template = None
        self.package_name = None
        self.subtemplates = []


@pytest.fixture(scope='module')
def config():
    config = Config()
    config.verbose = bool(os.environ.get('VERBOSE'))
    config.version = os.environ.get('VERSION', '5.1-latest')
    return config
