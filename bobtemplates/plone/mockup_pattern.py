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

    demo_path = os.path.join(
        configurator.variables["package.root_folder"], "resources/index.html"
    )
    configurator.variables["original_body"] = ""
    if os.path.exists(demo_path):
        with open(demo_path, "r") as demo_file:
            # Read the HTML file and extract the body
            demo_contents = demo_file.read()
            re_pattern = re.compile(r"\<body\>(.*)\<\/body\>", flags=re.DOTALL)
            configurator.variables["original_body"] = "".join(
                re_pattern.findall(demo_contents)
            )


def post_render(configurator):
    """"""
    git_init_status = git_init(configurator)
    if git_init_status:
        git_commit(
            configurator,
            "Add pattern: {0}".format(configurator.variables["pattern.name"]),
        )
    echo(
        """
Your pattern was added here: {0}/resources
Run 'npx yarn install' to get the dependencies.
Run 'npx yarn serve' to start the development server for developing your pattern.
Run 'npx yarn watch' to watch the pattern in the Plone environment and build it on changes.
and then 'npx yarn run build' to compile the javascript bundle for production.
""".format(
            configurator.variables["package.root_folder"],
        ),
        "info",
    )


def post_pattern_name(configurator, question, answer):
    regex = r"^\w+[a-zA-Z0-9\.\-_]*$"
    if not re.match(regex, answer):
        msg = "Error: '{0}' is not a valid pattern name.\n".format(answer)
        msg += "Please use a valid name (like 'Autoselect' or 'show-hide')!\n"
        msg += "At beginning or end only letters|digits are allowed.\n"
        msg += "Inside the name '.-_' are also allowed.\n"
        msg += "No accents or umlauts."
        raise ValidationError(msg)
    return answer
