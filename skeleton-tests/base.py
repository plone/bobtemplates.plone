# -*- coding: utf-8 -*-

# from bobtemplates.plone.utils import safe_encode
from bobtemplates.plone.utils import safe_unicode

import contextlib
import logging
import os
import subprocess


logger = logging.getLogger("skeleton-tests")


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
        returncode = subprocess.check_call(
            ['tox', '-r', '-e', config.skeleton_tox_env],
            cwd=wd,
        )
        # logger.debug(u'\n{0}\n'.format(safe_unicode(test_result)))
        return returncode
    except subprocess.CalledProcessError as execinfo:
        logger.debug(u'{0}'.format(safe_unicode(execinfo.output)))
        return execinfo.returncode
        # tox_msg = safe_unicode(execinfo.output)
        # print(tox_msg)
        # tox_summary = safe_unicode(
        #     b''.join(
        #         execinfo.output.partition(b'__ summary __')[1:],
        #     ),
        # )
        # assert execinfo.returncode == 0  #, u'\n{0}'.format(tox_msg)
