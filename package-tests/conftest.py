# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import os.path
import pytest
import shutil


@pytest.fixture(scope='module')
def buildpath():
    # setup
    buildpath = os.path.normpath(
        os.path.join(
            os.path.abspath(__file__),
            '..',
            '..',
            '_build',
            'package_tests',
        ),
    )
    print(buildpath)
    if not os.path.exists(buildpath):
        try:
            print('create Build-Path: {path}'.format(path=buildpath))
            os.makedirs(buildpath)
        except OSError as e:
            print(e)
    yield buildpath
    # tear down
    if os.path.exists(buildpath):
        print('delete Build-Path: {path}'.format(path=buildpath))
        shutil.rmtree(buildpath)
