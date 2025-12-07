from bobtemplates.plone import buildout
from mrbob.configurator import Configurator

import os


def test_prepare_renderer(tmpdir):
    target_path = tmpdir.strpath + "/collective.demo"
    package_path = target_path + "/src/collective/demo"
    os.makedirs(target_path)
    os.makedirs(package_path)
    configurator = Configurator(
        template="bobtemplates.plone:buildout",
        target_directory=package_path,
    )
    buildout.prepare_renderer(configurator)
    assert configurator.variables["template_id"] == "buildout"


def test_post_renderer():
    buildout.post_renderer(None)
