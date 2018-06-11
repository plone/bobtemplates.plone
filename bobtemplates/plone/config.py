# -*- coding: utf-8 -*-
"""Configure mrbob."""

from mrbob.bobexceptions import SkipQuestion

import os
import subprocess


home = os.path.expanduser('~')


def generate_answers_ini(path, template):
    with open(os.path.join(path, '.mrbob'), 'w') as f:
        f.write(template)


def check_git_init(configurator, answer):
    if configurator.variables['package.git.init']:
        raise SkipQuestion(
            u'GIT is not initialize, so we skip autocommit question.',
        )


def configure(configurator):
    template = """[mr.bob]
verbose = False
[variables]
author.name={0}
author.email={1}
author.github.user={2}
plone.version={3}
package.git.init={4}
package.git.autocommit={5}
package.git.disabled={6}
""".format(
        configurator.variables['author.name'],
        configurator.variables['author.email'],
        configurator.variables['author.github.user'],
        configurator.variables['plone.version'],
        configurator.variables['package.git.init'],
        configurator.variables['package.git.autocommit'],
        configurator.variables['package.git.disabled'],
    )
    generate_answers_ini(home, template)
    subprocess.call(
        [
            'mrbob',
            '--config', 'answers.ini',
        ],
        cwd=home,
    )
