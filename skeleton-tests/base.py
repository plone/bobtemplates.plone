# -*- coding: utf-8 -*-

from bobtemplates.eea.utils import safe_unicode

import contextlib
import os
import subprocess


@contextlib.contextmanager
def dummy_contextmanager():
    yield None


def generate_answers_ini(path, template):
    with open(os.path.join(path, 'answers.ini'), 'w') as f:
        f.write(template)


def file_exists(base_path, file_path):
    is_file = os.path.isfile(base_path + file_path)
    return is_file


def run_skeleton_tox_env(wd, config):
    try:
        test_result = subprocess.check_output(
            ['tox', '-e', config.skeleton_tox_env],
            cwd=wd,
        )
        print(u'\n{0}\n'.format(safe_unicode(test_result)))
    except subprocess.CalledProcessError as execinfo:
        tox_msg = safe_unicode(
            b''.join(bytes(execinfo.output)),
        )
        print(tox_msg)
        tox_summary = safe_unicode(
            b''.join(
                execinfo.output.partition(b'__ summary __')[1:],
            ),
        )
        assert execinfo.returncode == 0, '\n{0}'.format(tox_summary)
