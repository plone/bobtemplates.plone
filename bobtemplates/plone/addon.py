import json
import os
import shutil
import subprocess


def pre_render(configurator):
    """Some variables to make templating easier."""
    package_dir = os.path.basename(configurator.target_directory)
    namespaces = package_dir.replace("-", "_").split(".")
    backend_addon_data = {
        "default_context": {
            "title": ".".join(namespaces),
            "python_package_name": ".".join(namespaces),
            "author": configurator.variables.get("author.name") or "Dummy",
            "email": configurator.variables.get("author.email")
            or "collective@plone.org",
            "github_organization": configurator.variables.get("author.github.user")
            or "collective",
            "plone_version": configurator.variables.get("plone.version") or "6.1.2",
        }
    }

    # prepare the answers file for cookieplone
    with open("answers.json", "w") as fp:
        json.dump(backend_addon_data, fp)

    # mr.bob creates the folder, but we need cookieplone to create it
    # so we delete it here :/
    shutil.rmtree(package_dir)

    subprocess.run([
        "uvx",
        "cookieplone",
        "backend_addon",
        "--no-input",
        "--config-file",
        "answers.json",
    ])


def pre_ask(configurator):
    """ """


def post_render(configurator):
    print("Done")
