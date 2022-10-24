# -*- coding: utf-8 -*-
from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import echo
from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import git_init
from mrbob.bobexceptions import ValidationError

import os
import re


def pre_render(configurator):
    """Prepare configuration variables."""
    configurator = base_prepare_renderer(configurator)
    configurator.variables["template_id"] = "mockup_pattern"

    bundle_js_path = os.path.join(
        configurator.variables["package.root_folder"], "resources/bundle.js"
    )
    configurator.variables["original_imports"] = ""
    if os.path.exists(bundle_js_path):
        with open(bundle_js_path, "r") as bundle_js:
            configurator.variables["original_imports"] = "\n".join(
                [
                    line.strip()
                    for line in bundle_js.readlines()
                    if "import" in line and "patternslib" not in line
                ]
            )

    configurator.variables["original_body"] = value_from_template(
        configurator.variables["package.root_folder"],
        "resources/index.html",
        r"\<body\>(.*)\<\/body\>",
    )

    configurator.variables["original_browser_configure"] = value_from_template(
        configurator.variables["package_folder"],
        "browser/configure.zcml",
        r"(\<configure.*)\<\/configure\>",
    )

    configurator.variables["original_browser_template"] = (
        value_from_template(
            configurator.variables["package_folder"],
            "browser/pattern-demo.pt",
            r"<metal:block define-macro=\"content-core\"\>(.*)\<\/metal:block\>",
        )
        or ""
    )


def value_from_template(root_folder, relative_path, regex):
    path = os.path.join(root_folder, relative_path)
    if os.path.exists(path):
        with open(path, "r") as file:
            # Read the HTML file and extract the body
            contents = file.read()
            re_pattern = re.compile(regex, flags=re.DOTALL)
            return "".join(re_pattern.findall(contents))


def post_render(configurator):
    """Post render script."""
    root_folder = configurator.variables["package.root_folder"]
    pattern_name = configurator.variables["pattern.name"]
    package_name = configurator.variables["package.name"]
    package_folder_rel_path = configurator.variables["package_folder_rel_path"]

    git_init_status = git_init(configurator)
    if git_init_status:
        git_commit(
            configurator,
            f"Add pattern: {pattern_name}",
        )
    echo(
        f"""
Your pattern was added here: {root_folder}/resources/pat-{pattern_name}

Run "npx yarn install" to get the dependencies.
Run "npx yarn start" to start the development server for developing your pattern.
Run "npx yarn watch" to re-build the pattern into the Plone environment on changes.
Run "npx yarn run build" to compile the javascript bundle for production.

Note: You need to build the bundle before you can use the pattern in Plone.

Note: You might want to edit and fix the following file - there might be multiple
      "{package_name}-pattern-demo" view configurations in it:

.{package_folder_rel_path}/browser/configure.zcml

There is a demo view for your pattern at:

http://localhost:8080/Plone/@@{package_name}-pattern-demo

""",
        "info",
    )


def post_pattern_name(configurator, question, answer):
    """Check name."""
    regex = r"^\w+[a-zA-Z0-9\.\-_]*$"
    if not re.match(regex, answer):
        msg = f"""Error: "{answer}" is not a valid pattern name.
Please use a valid name (like "Autoselect" or "show-hide")!
At beginning or end only letters|digits are allowed.
Inside the name ".-_" are also allowed.
No accents or umlauts."""
        raise ValidationError(msg)
    return answer
