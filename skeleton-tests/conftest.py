import os
import pytest


class Config:
    def __init__(self):
        self.version = None
        self.verbose = None
        self.template = None
        self.skeleton_tox_env = None
        self.package_name = None
        self.subtemplates = []


@pytest.fixture(scope="module")
def config():
    skeleton_tox_env_parts = os.environ.get("ENVNAME").split("-")
    config = Config()
    config.verbose = bool(os.environ.get("VERBOSE"))
    config.version = os.environ.get("VERSION", "5.2.1")
    config.skeleton_tox_env = f"{skeleton_tox_env_parts[0]}-{skeleton_tox_env_parts[2]},{skeleton_tox_env_parts[0]}-lint"
    return config
