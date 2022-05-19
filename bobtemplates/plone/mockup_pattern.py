# -*- coding: utf-8 -*-
import os
import re

from mrbob.bobexceptions import ValidationError

from bobtemplates.plone.base import base_prepare_renderer, echo, git_commit, git_init


def pre_render(configurator):
    """ """
    configurator = base_prepare_renderer(configurator)
    configurator.variables["template_id"] = "mockup_pattern"
    bundle_js_path = os.path.join(
        configurator.variables["package.root_folder"], "resources/patterns/bundle.js"
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


def post_render(configurator):
    """ """
    git_init_status = git_init(configurator)
    if git_init_status:
        git_commit(
            configurator,
            "Add pattern: {0}".format(configurator.variables["pattern.name"]),
        )
    echo(
        """\nYour pattern was added here: {0}/resources
Run 'npx yarn install' to get the dependencies
        and then 'npx yarn run watch:webpack' to compile the javascript bundle.
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
