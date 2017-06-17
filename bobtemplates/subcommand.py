from mrbob.bobexceptions import ValidationError
import keyword
import logging
import re
import os

log = logging.getLogger("bobtemplates.plone")


def _get_package_root_folder():
    file_name = 'setup.py'
    cur_dir = os.getcwd()
    while True:
        files = os.listdir(cur_dir)
        parent_dir = os.path.dirname(cur_dir)
        if file_name in files:
            break
        else:
            if cur_dir == parent_dir:
                break
            cur_dir = parent_dir
    return cur_dir


def check_dexterity_type_name(configurator, question, answer):
    if keyword.iskeyword(answer):
        raise ValidationError('%s is a reserved Python keyword' % answer)
    if not re.match('[_a-zA-Z ]*$', answer):
        raise ValidationError('%s is not a valid identifier' % answer)
    return answer


def prepare_render(configurator):
    """ Some variables to make templating easier.
    """
    # TODO: find out package.dottedname from parent package:
    root_folder = _get_package_root_folder()
    configurator.variables['package.dottedname'] = root_folder.split('/')[-1]
    type_name = configurator.variables['dexterity_type_name']
    configurator.variables[
        'dexterity_type_name_klass'] = type_name.title().replace(' ', '')
    configurator.variables[
        'dexterity_type_name_normalized'] = type_name.replace(' ', '_').lower()


def post_renderer(configurator):
    """
    """
    print("""vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

Now add the follwing to profiles/default/types.xml:

    <object name="%s" meta_type="Dexterity FTI"/>
    """ % configurator.variables['dexterity_type_name_normalized'])
