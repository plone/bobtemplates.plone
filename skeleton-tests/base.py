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
    with open(os.path.join(path, "answers.ini"), "w") as f:
        f.write(template)


def file_exists(base_path, file_path):
    is_file = os.path.isfile(base_path + file_path)
    return is_file


def run_skeleton_tox_env(wd, config):
    logger.info("show_versions: python / tox")
    print("show_versions: python / tox")
    subprocess.check_call(
        ["python", "--version"],
        cwd=wd,
    )
    subprocess.check_call(
        ["tox", "--version"],
        cwd=wd,
    )
    try:
        returncode = subprocess.check_call(
            ["tox", "-e", config.skeleton_tox_env, "-p", "auto", "-o", "-v", "-r"],
            cwd=wd,
        )
        return returncode
    except subprocess.CalledProcessError as execinfo:
        logger.debug("{0}".format(safe_unicode(execinfo.output)))
        return execinfo.returncode
