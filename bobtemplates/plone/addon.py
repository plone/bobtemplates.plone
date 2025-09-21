from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import git_init
from bobtemplates.plone.base import make_path
from bobtemplates.plone.utils import run_black
from bobtemplates.plone.utils import run_isort

import json
import os
import shutil
import subprocess



def pre_render(configurator):
    """Some variables to make templating easier."""
    package_dir = os.path.basename(configurator.target_directory)
    namespaces = package_dir.replace("-", "_").split(".")
    backend_addon_data = {
        "default_context":{
            "title": ".".join(namespaces),
            "python_package_name": ".".join(namespaces),
            "author": configurator.variables['author.name'],
            "email": configurator.variables['author.email'],
            "github_organization": configurator.variables['author.github.user'] or 'collective',
            "plone_version": configurator.variables['plone.version']
        }
    }

    try:
        os.makedirs(package_dir)
    except:
        pass

    with open(f'{package_dir}/answers.json', 'w') as fp:
        json.dump(backend_addon_data, fp)

    os.chdir(package_dir)
    subprocess.run(["uvx", "cookieplone", "backend_addon", "--no-input", "--config-file", "answers.json"])

def pre_ask(configurator):
    """ """

def post_render(configurator):
    print("Done")