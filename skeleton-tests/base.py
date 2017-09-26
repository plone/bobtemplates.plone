# -*- coding: utf-8 -*-

import contextlib
import os


@contextlib.contextmanager
def dummy_contextmanager():
    yield None


def generate_answers_ini(path, template):
    with open(os.path.join(path, 'answers.ini'), 'w') as f:
        f.write(template)


def file_exists(base_path, file_path):
    is_file = os.path.isfile(base_path + file_path)
    return is_file
