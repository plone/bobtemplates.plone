# -*- coding: utf-8 -*-

import os


def init_package_base_files(configurator):
    target_path = configurator.variables.get(u'package.root_folder')
    u""" prepare base files, expected in a addon package by sub-templates.
    """
    template = """
[main]
version=5.1
"""
    with open(os.path.join(target_path + '/bobtemplate.cfg'), 'w') as f:
        f.write(template)

    template = """
    dummy
    '-*- Extra requirements: -*-'
"""
    with open(os.path.join(target_path + '/setup.py'), 'w') as f:
        f.write(template)
