# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import shutil
import subprocess

test_answers_dir = 'test_answers'
test_answers_file = 'test_answers'

test_scripts_dir = 'test_scripts'
test_scripts_file = 'test_script'

SOURCE = {
    'package.namespace': ['collective'],
    'package.namespace2': ['bar', ''],
    'package.name': ['foo'],
    'author.name': ['Mister Böb'],
    'author.email': ['mrbob@plone.org'],
    'author.github.user': ['mrbob'],
    'package.description': ['An add-on for Plone'],
    'plone.version': ['4.3.4', '5.0a3'],
    'package.example': [True, False],
    'package.theme': [False, True],
    'plone.is_plone5': [False],
    'python.version': [2.7],
}

SCRIPT_STRING = """#!/bin/sh
set -e
{local_dir}/bin/mrbob -O {package} bobtemplates:plone_addon --config {ini}
cd {local_dir}/{package}
python bootstrap-buildout.py --setuptools-version=8.3
{local_dir}/{package}/bin/buildout
{local_dir}/{package}/bin/test
{local_dir}/{package}/bin/code-analysis
rm -rf {local_dir}/{package}/"""


def combine(list_a, combinations):
    retval = []
    for a in list_a:
        for b in combinations:
            retval.append(b + [a])
    return retval


def is_plone5(version):
    if version.startswith('5'):
        return True
    return False


def generate_all_combinations():
    keys = SOURCE.keys()
    first = SOURCE[keys[0]]
    combinations = [[x] for x in first]
    for key in keys[1:]:
        combinations = combine(SOURCE[key], combinations)
    combinations = [dict(zip(keys, x)) for x in combinations]
    return combinations


def run_test_scripts(directory):
    to_purge = ['collective.bar.foo', 'collective.foo']
    results = []
    for test_script in os.listdir(directory):
        command = '{0}/{1}'.format(directory, test_script)
        try:
            status = subprocess.call(command)
            results.append(status)
        except OSError:
            print('Error: {} does not exist!'.format(command))
        finally:
            for path in to_purge:
                if os.path.exists(path):
                    shutil.rmtree(path)
    return results


def main():
    """Create all possible test_answers_files and the test-scripts using them.
    """
    # Set Plone-version
    all_combinations = generate_all_combinations()
    for i in all_combinations:
        i['plone.is_plone5'] = is_plone5(i['plone.version'])

    # Cleanup (start fresh)
    local_dir = os.path.split(os.path.realpath(__file__))[0]
    if os.path.exists(test_answers_dir) and os.path.isdir(test_answers_dir):
        shutil.rmtree(test_answers_dir)
    os.makedirs(test_answers_dir)
    if os.path.exists(test_scripts_dir) and os.path.isdir(test_scripts_dir):
        shutil.rmtree(test_scripts_dir)
    os.makedirs(test_scripts_dir)

    for index, combination in enumerate(all_combinations, start=1):
        answers_file_path = '{0}/{1}_{2}.ini'.format(
            test_answers_dir,
            test_answers_file,
            index)
        f = open(answers_file_path, 'a')
        print('[variables]', file=f)
        for k, v in combination.items():
            print_line = '{0} = {1}'.format(k, v)
            print(print_line, file=f)
        f.close()

        if combination['package.namespace2']:
            package_name = '{0}.{1}.{2}'
        else:
            package_name = '{0}.{2}'
        package_name = package_name.format(
            combination['package.namespace'],
            combination['package.namespace2'],
            combination['package.name'])
        script_string = SCRIPT_STRING.format(
            local_dir=local_dir,
            package=package_name,
            ini=answers_file_path
        )
        script_path = '{0}/{1}_{2}'.format(
            test_scripts_dir,
            test_scripts_file,
            index)
        f = open(script_path, 'a')
        print(script_string, file=f)
        f.close()
        os.chmod(script_path, 0755)
    results = run_test_scripts(test_scripts_dir)
    print(results)


if __name__ == '__main__':
    main()
