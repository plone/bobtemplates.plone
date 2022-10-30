from bobtemplates.plone.base import git_commit, git_support
from bobtemplates.plone.base import base_prepare_renderer


def prepare_renderer(configurator):
    """Prepare rendering."""
    configurator = base_prepare_renderer(configurator)

    configurator.target_directory = configurator.variables["package_folder"]


def post_renderer(configurator):
    """Post rendering."""
    if git_support(configurator):
        git_commit(configurator, "Add starter configuration")
