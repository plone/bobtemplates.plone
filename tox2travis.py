# -*- coding: utf-8 -*-

from tox.config import parseconfig


print('matrix:')
print('    include:')
for env in parseconfig(None, 'tox').envlist:
    if not env.startswith('coverage'):
        print('        - env: TOXENV={0}'.format(env))
        if env.startswith('py37'):
            print('          python: "3.7"')


#    include:
#        - python: "2.7"
#          env: TOXENV=lint-py27,docs
