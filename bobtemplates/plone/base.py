from colorama import Fore
from colorama import Style
from datetime import date
from lxml import etree
from mrbob import hooks
from mrbob.bobexceptions import MrBobError
from mrbob.bobexceptions import SkipQuestion
from mrbob.bobexceptions import ValidationError
from mrbob.rendering import jinja2_env
from six.moves import input as six_input

import case_conversion as cc
import codecs
import keyword
import os
import six
import string
import subprocess
import sys
import tomllib


try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser


ZCML_NAMESPACES = {
    "browser": "http://namespaces.zope.org/browser",
    "plone": "http://namespaces.plone.org/plone",
}


CONTENT_TYPE_INTERFACES = {
    "*": "*",
    "Document": "plone.app.contenttypes.interfaces.IDocument",
    "Folder": "plone.app.contenttypes.interfaces.IFolder",
    "Collection": "plone.app.contenttypes.interfaces.ICollection",
    "Event": "plone.app.contenttypes.interfaces.IEvent",
    "News Items": "plone.app.contenttypes.interfaces.INewsItem",
}


def to_boolean(value):
    if not value:
        return False
    if isinstance(value, six.string_types):
        value = hooks.to_boolean(None, None, value)
    else:
        value = bool(value)
    return value


# this is a custom filter which we can use in jinja template.
# see https://github.com/plone/bobtemplates.plone/issues/292
jinja2_env.filters["to_boolean"] = to_boolean


def git_support_enabled(configurator, question):
    disabled = configurator.variables.get("package.git.disabled", "False")
    if hooks.to_boolean(None, None, disabled):
        echo("GIT support disabled!!!")
        raise SkipQuestion("GIT support is disabled, skip question!")


def echo(msg, msg_type=None):
    if not isinstance(msg, six.string_types):
        msg = str(msg)
    if msg_type == "warning":
        colored_msg = Fore.YELLOW + msg + Style.RESET_ALL
    if msg_type == "error":
        colored_msg = Fore.RED + msg + Style.RESET_ALL
    if msg_type == "info":
        colored_msg = Fore.GREEN + Style.DIM + msg + Style.RESET_ALL
    if not msg_type:
        colored_msg = msg + Style.RESET_ALL
    print(colored_msg)


class BobConfig:
    def __init__(self):
        self.version = None
        self.git_init = None
        self.template = None
        self.package_dottedname = None


def git_support(configurator):
    """check if GIT support is disabled/enabled"""
    git_support = True
    disabled = configurator.variables.get("package.git.disabled", "False")
    if hooks.to_boolean(None, None, disabled):
        echo("GIT support disabled!")
        git_support = False
    return git_support


def git_init(configurator):
    if not git_support(configurator):
        return
    git_init_flag = configurator.variables.get("package.git.init", "False")
    if not hooks.to_boolean(None, None, str(git_init_flag)):
        echo("git init is disabled!")
        return
    params = ["git", "init"]
    echo("RUN: {0}".format(" ".join(params)), "info")
    try:
        result = subprocess.check_output(params, cwd=configurator.target_directory)
    except subprocess.CalledProcessError as e:
        echo(e.output, "warning")
    else:
        if result:
            echo(result, "info")
    return True


def git_commit(configurator, msg):
    if not git_support(configurator):
        return
    non_interactive = configurator.bobconfig.get("non_interactive")
    working_dir = (
        configurator.variables.get("package.root_folder")
        or configurator.target_directory
    )
    params1 = ["git", "add", "."]
    params2 = ["git", "commit", "-m", f"{msg}"]
    git_autocommit = None
    run_git_commit = True
    autocommit_flag = configurator.variables.get("package.git.autocommit", "False")
    if hooks.to_boolean(None, None, autocommit_flag):
        git_autocommit = True
    if not non_interactive and not git_autocommit:
        echo(
            "Should we run?:\n{0}\n{1}\nin: {2}".format(
                " ".join(params1), " ".join(params2), working_dir
            ),
            "info",
        )
        run_git_commit = (six_input("[y]/n: ") or "y").lower() == "y"

    if not run_git_commit and not git_autocommit:
        echo("Skip git commit!", "warning")
        return

    echo("RUN: {0}".format(" ".join(params1)), "info")
    try:
        result1 = subprocess.check_output(params1, cwd=working_dir)
    except subprocess.CalledProcessError as e:
        echo(e.output, "warning")
    else:
        if result1:
            echo(result1, "info")

    echo("RUN: {0}".format(" ".join(params2)), "info")
    try:
        result2 = subprocess.check_output(params2, cwd=working_dir)
    except subprocess.CalledProcessError as e:
        echo(e.output, "warning")
    else:
        echo(result2, "info")


def git_clean_state_check(configurator, question):
    if not git_support(configurator):
        return
    params = ["git", "status", "--porcelain", "--ignore-submodules"]
    echo("\nRUN: {0}".format(" ".join(params)), "info")
    try:
        result = subprocess.check_output(params, cwd=configurator.target_directory)
    except subprocess.CalledProcessError as e:
        echo(e.output, "error")
    else:
        if not result:
            echo("Git state is clean.\n", "info")
            raise SkipQuestion("Git state is clean, so we skip this question.")
        echo(
            f"git status result:\n----------------------------\n{result}",
            "warning",
        )


def check_klass_name(configurator, question, answer):
    if keyword.iskeyword(answer):
        raise ValidationError(f"{answer} is a reserved Python keyword")
    if not answer.isidentifier():
        raise ValidationError(f"{answer} is not a valid class identifier")
    return answer


def check_method_name(configurator, question, answer):
    if keyword.iskeyword(answer):
        raise ValidationError(f"{answer} is a reserved Python keyword")
    if not answer.isidentifier():
        raise ValidationError(f"{answer} is not a valid method identifier")
    return answer


def read_bobtemplates_ini(configurator):
    bob_config = BobConfig()
    config = ConfigParser()
    path = configurator.target_directory + "/bobtemplate.cfg"
    config.read(path)
    if not config.sections():
        return
    bob_config.version = config.get("main", "version")
    bob_config.git_init = None
    if config.has_option("main", "git_init"):
        bob_config.git_init = config.get("main", "git_init")
    if config.has_option("main", "package.dottedname"):
        bob_config.package_dottedname = config.get("main", "package.dottedname")
    return bob_config


def set_global_vars(configurator):
    bob_config = read_bobtemplates_ini(configurator)
    configurator.variables["year"] = date.today().year
    version = configurator.variables.get("plone.version")
    if not version and bob_config:
        print(">>> reading Plone version from bobtemplate.cfg")
        version = bob_config.version
    configurator.variables["plone.version"] = version
    set_plone_version_variables(configurator)
    if hasattr(bob_config, "package_dottedname"):
        configurator.variables["package.dottedname"] = bob_config.package_dottedname


def set_plone_version_variables(configurator, answer=None):
    version = configurator.variables.get("plone.version", answer)
    if not version:
        return
    if "plone.is_plone5" not in configurator.variables:
        # Find out if it is supposed to be Plone 5.0 or higher
        configurator.variables["plone.is_plone5"] = version.startswith("5")
    if "plone.is_plone51" not in configurator.variables:
        # Find out if it is supposed to be Plone 5.1
        configurator.variables["plone.is_plone51"] = version.startswith("5.1")
    if "plone.is_plone52" not in configurator.variables:
        # Find out if it is supposed to be Plone 5.2
        configurator.variables["plone.is_plone52"] = version.startswith("5.2")
    if "plone.minor_version" not in configurator.variables:
        # extract minor version (4.3)
        # (according to https://plone.org/support/version-support-policy)
        # this is used for the trove classifier in setup.py of the product
        configurator.variables["plone.minor_version"] = ".".join(version.split(".")[:2])


def get_git_info(value):
    """Try to get information from the git-config."""
    gitargs = [b"git", b"config", b"--get"]
    try:
        result = subprocess.check_output(*gitargs, [value]).strip()
        if isinstance(result, six.binary_type):
            result = result.decode("utf8")
        return result
    except (OSError, subprocess.CalledProcessError):
        return "FakeGitUserOrEmail"


def validate_packagename(configurator):
    """Find out if the name target-dir entered when invoking the command can be
    a valid python-package."""
    package_dir = os.path.basename(configurator.target_directory)
    fail = False

    allowed = set(string.ascii_letters + string.digits + ".-_")
    if not set(package_dir).issubset(allowed):
        fail = True

    if package_dir.startswith(".") or package_dir.endswith("."):
        fail = True

    for namespace in package_dir.replace("-", "_").split("."):
        if keyword.iskeyword(namespace) or not namespace.isidentifier():
            fail = True

    if fail:
        msg = (
            f"Error: '{package_dir}' is not a valid packagename.\n"
            "Please use a valid name (like collective.myaddon or "
            "plone.app.myaddon)"
        )
        sys.exit(msg)


def post_plone_version(configurator, question, answer):
    """Find out if it is supposed to be Plone 5."""
    set_plone_version_variables(configurator, answer)
    return answer


def pre_username(configurator, question):
    """Get email from git and validate package name."""
    # validate_packagename should be run before asking the first question.
    validate_packagename(configurator)

    default = get_git_info("user.name")
    if default and question:
        question.default = default


def pre_email(configurator, question):
    """Get email from git."""
    default = get_git_info("user.email")
    if default and question:
        question.default = default


def is_string_in_file(configurator, file_path, match_str):
    """Simple check if a given string is in a file.

    You can use this before adding new lines with update_file.

    """
    with open(file_path, "r+") as xml_file:
        contents = xml_file.readlines()
    return any(match_str in line for line in contents)


def make_path(*args):
    """generate path string."""
    return os.sep.join(args)


def update_configure_zcml(
    configurator,
    path,
    file_name=None,
    example_file_name=None,
    match_xpath=None,
    match_str=None,
    insert_str=None,
):
    if path[-1] != "/":
        path += "/"
    file_path = os.path.join(path, file_name)
    if example_file_name:
        example_file_path = os.path.join(path, example_file_name)
        file_list = os.listdir(os.path.dirname(path))
        if file_name not in file_list:
            print("rename example zcml file")
            os.rename(example_file_path, file_path)
    namespaces = {
        "zope": "http://namespaces.zope.org/zope",
        "gs": "http://namespaces.zope.org/genericsetup",
        "i18n": "http://namespaces.zope.org/i18n",
        "plone": "http://namespaces.plone.org/plone",
    }
    with open(file_path) as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        if len(tree.xpath(match_xpath, namespaces=namespaces)):
            print(f"{insert_str} already in {file_path}, skip adding!")
            return
    update_file(configurator, file_path, match_str, insert_str)


def update_file(configurator, file_path, match_str, insert_str):
    """Insert insert_str into given file, by match_str."""
    changed = False
    with codecs.open(file_path, "r+", encoding="utf-8") as xml_file:
        contents = xml_file.readlines()
        if match_str in contents[-1]:  # Handle last line, prev. IndexError
            contents.append(insert_str)
            changed = True
        else:
            for index, line in enumerate(contents):
                if match_str in line and insert_str not in contents[index + 1]:
                    contents.insert(index + 1, insert_str)
                    changed = True
                    break
        xml_file.seek(0)
        xml_file.writelines(contents)

    if not changed:
        print(
            f"WARNING: We couldn't find the match_str, skip inserting into: {file_path}"
        )


def _get_package_root_folder(configurator):
    file_names = ["setup.py", "bobtemplate.cfg", "pyproject.toml"]
    root_folder = None
    os.chdir(configurator.target_directory)
    cur_dir = os.getcwd()

    while True:
        files = os.listdir(cur_dir)
        parent_dir = os.path.dirname(cur_dir)
        for file_name in file_names:
            if file_name in files:
                root_folder = cur_dir
        if root_folder:
            break
        else:
            if cur_dir == parent_dir:
                break
            cur_dir = parent_dir
    if not root_folder:
        raise MrBobError(
            "No package root folder found in path!\n"
            "Please make sure you have one of the following files:"
            " setup.py, bobtemplate.cfg, pyproject.toml in your package root"
        )
    return root_folder


def check_root_folder(configurator, question):
    """Check if we are in a package.

    Should be called in first question pre hook.

    """
    root_folder = _get_package_root_folder(configurator)
    if not root_folder:
        raise ValidationError(
            "\n\nNo setup.py found in path!\n"
            "Please run this subtemplate inside an existing package,\n"
            "in the package dir, where the actual code is!\n"
            "In the package collective.dx it's in collective.dx/collective/dx"
            "\n"
        )


def dottedname_to_path(dottedname):
    path = "/".join(dottedname.split("."))
    return path


def setuppy_has_package_dir(configurator):
    package_root_folder = _get_package_root_folder(configurator)
    os.chdir(package_root_folder)
    cur_dir = os.getcwd()
    files = os.listdir(cur_dir)
    if "setup.py" not in files:
        return False
    with open("setup.py") as file:
        line = file.readline()
        while line:
            if "package_dir" in line:
                return True
            line = file.readline()
    return False


def pyproject_has_package_dir(configurator):
    """ """
    package_root_folder = _get_package_root_folder(configurator)
    os.chdir(package_root_folder)
    cur_dir = os.getcwd()
    files = os.listdir(cur_dir)
    if "pyproject.toml" not in files:
        return False

    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
        # tool.hatch.build.targets.wheel
        tool = data.get("tool")
        if not tool:
            return False
        hatch = tool.get("hatch")
        if not hatch:
            return False
        build = hatch.get("build")
        if not build:
            return False
        targets = build.get("targets")
        if not targets:
            return False
        wheel = targets.get("wheel")
        if not wheel:
            return False
        packages = wheel.get("packages")
        if not packages:
            return False
        # for package in packages:
        #     if "src/" in package:
        #         return True
        return any("src/" in package for package in packages)
        return False


def get_package_folder_rel_path(configurator):
    """read pyproject or setup.py to determent the package_folder"""
    package_subpath = dottedname_to_path(configurator.variables["package.dottedname"])
    if setuppy_has_package_dir(configurator) or pyproject_has_package_dir(configurator):
        package_folder_rel_path = "/src/" + package_subpath
    else:
        package_folder_rel_path = "/" + package_subpath
    return package_folder_rel_path


def base_prepare_renderer(configurator):
    """generic rendering before template specific rendering."""
    configurator.variables["package.root_folder"] = _get_package_root_folder(
        configurator
    )
    # run this before setting more variables:
    set_global_vars(configurator)

    if not configurator.variables.get("package.dottedname"):
        configurator.variables["package.dottedname"] = configurator.variables[
            "package.root_folder"
        ].split(os.path.sep)[-1]

    configurator.variables["package.namespace"] = configurator.variables[
        "package.dottedname"
    ].split(".")[0]

    configurator.variables["package.name"] = configurator.variables[
        "package.dottedname"
    ].split(".")[-1]

    configurator.variables["package.uppercasename"] = (
        configurator.variables["package.dottedname"].replace(".", "_").upper()
    )

    configurator.variables["package_folder_rel_path"] = get_package_folder_rel_path(
        configurator
    )
    configurator.variables["package_folder"] = (
        f"{configurator.variables['package.root_folder']}{configurator.variables['package_folder_rel_path']}"
    )

    configurator.target_directory = configurator.variables["package.root_folder"]

    if "package.browserlayer" not in configurator.variables:
        camelcasename = (
            configurator.variables["package.dottedname"]
            .replace(".", " ")
            .title()
            .replace(" ", "")
            .replace("_", "")
        )
        browserlayer = f"{camelcasename}Layer"
        configurator.variables["package.browserlayer"] = browserlayer

    return configurator


def remove_unwanted_files(file_paths):
    for file_path in file_paths:
        if not os.path.isfile(file_path):
            continue
        os.remove(file_path)


def subtemplate_warning(configurator, question):
    """Show a warning to the user before using subtemplates!"""
    print(
        """
    ### WARNING ###

    This is a subtemplate, it might override existing files without warnings!
    Please use a version control system like GIT with a clean state,
    to track changes, before using this subtemplate!

    """,
    )


def subtemplate_warning_post_question(configurator, question, answer):
    if answer.lower() != "y":
        print("Abort!")
        sys.exit(0)
    return answer


def get_normalized_dxtypename(name):
    normalized_name = cc.snakecase(get_normalized_ftiname(name))
    return normalized_name


def get_normalized_classname(name):
    normalized_name = cc.pascalcase(name)
    return normalized_name


def get_normalized_ftiname(name):
    normalized_name = name.replace(" ", "_")
    return normalized_name


def get_normalized_themename(name):
    name = name.replace("(", "")
    name = name.replace(")", "")
    name = name.replace("-", "")
    name = name.replace(" ", "_")
    normalized_name = cc.dashcase(name)
    return normalized_name
