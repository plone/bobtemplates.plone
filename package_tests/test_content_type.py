"""Test dexterity content type generation."""

from .base import SETUPPY_TEMPLATE
from bobtemplates.plone import base
from bobtemplates.plone import content_type
from mrbob.bobexceptions import SkipQuestion
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator

import os
import pytest


def test_post_dexterity_type_name():
    """Test validation of entered dexterity type names."""

    def hookit(value):
        return content_type.check_dexterity_type_name(None, None, value)

    with pytest.raises(ValidationError):
        hookit("import")
    # Python 3.0 introduces additional characters from outside the ASCII range (see PEP 3131).
    # with pytest.raises(ValidationError):
    #     hookit("süpertype")
    #    with pytest.raises(ValidationError):
    #        hookit(u'Staff Member')
    with pytest.raises(ValidationError):
        hookit("2ndComing")
    #    with pytest.raises(ValidationError):
    #        hookit(u'Second Coming')
    with pytest.raises(ValidationError):
        hookit("*sterisk")
    with pytest.raises(ValidationError):
        hookit("da-sh")
    assert hookit("SuperType") == "SuperType"
    assert hookit("Super Type") == "Super Type"
    assert hookit("second_coming") == "second_coming"
    assert hookit("second coming") == "second coming"


def test_is_container_false():
    configurator = Configurator(
        template="bobtemplates.plone:content_type",
        target_directory="collective.foo.bar",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "dexterity_type_base_class": "Item",
        },
    )
    with pytest.raises(SkipQuestion):
        content_type.is_container(configurator, None)


def test_is_container_true():
    configurator = Configurator(
        template="bobtemplates.plone:content_type",
        target_directory="collective.foo.bar",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "dexterity_type_base_class": "Container",
        },
    )
    content_type.is_container(configurator, None)


def test_prepare_renderer(tmpdir):
    """Test prepare renderer."""
    target_dir = tmpdir.strpath + "/collective.foo.bar"
    os.mkdir(target_dir)
    template = SETUPPY_TEMPLATE
    with open(os.path.join(target_dir + "/setup.py"), "w") as f:
        f.write(template)

    configurator = Configurator(
        template="bobtemplates.plone:content_type",
        target_directory="collective.foo.bar",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "dexterity_type_name": "Special Task",
        },
    )
    content_type.prepare_renderer(configurator)
    assert configurator.variables["dexterity_type_name"] == "Special Task"
    assert configurator.variables["dexterity_type_fti_file_name"] == "Special_Task"
    assert configurator.variables["dexterity_type_name_klass"] == "SpecialTask"
    assert configurator.variables["dexterity_type_name_normalized"] == "special_task"
    assert configurator.target_directory.endswith(
        "/collective.todo/src/collective/todo"
    )

    configurator = Configurator(
        template="bobtemplates.plone:content_type",
        target_directory="collective.foo.bar",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "dexterity_type_name": "SpecialTask",
        },
    )
    content_type.prepare_renderer(configurator)
    assert configurator.variables["dexterity_type_name"] == "SpecialTask"
    assert configurator.variables["dexterity_type_fti_file_name"] == "SpecialTask"
    assert configurator.variables["dexterity_type_name_klass"] == "SpecialTask"
    assert configurator.variables["dexterity_type_name_normalized"] == "special_task"
    assert configurator.target_directory.endswith(
        "/collective.todo/src/collective/todo"
    )

    configurator = Configurator(
        template="bobtemplates.plone:content_type",
        target_directory="collective.foo.bar",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "dexterity_type_name": "special task",
        },
    )
    content_type.prepare_renderer(configurator)
    assert configurator.variables["dexterity_type_name"] == "special task"
    assert configurator.variables["dexterity_type_fti_file_name"] == "special_task"
    assert configurator.variables["dexterity_type_name_klass"] == "SpecialTask"
    assert configurator.variables["dexterity_type_name_normalized"] == "special_task"
    assert configurator.target_directory.endswith(
        "/collective.todo/src/collective/todo"
    )

    configurator = Configurator(
        template="bobtemplates.plone:content_type",
        target_directory="collective.foo.bar",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "dexterity_type_name": "Special_Task",
        },
    )
    content_type.prepare_renderer(configurator)
    assert configurator.variables["dexterity_type_name"] == "Special_Task"
    assert configurator.variables["dexterity_type_fti_file_name"] == "Special_Task"
    assert configurator.variables["dexterity_type_name_klass"] == "SpecialTask"
    assert configurator.variables["dexterity_type_name_normalized"] == "special_task"
    assert configurator.target_directory.endswith(
        "/collective.todo/src/collective/todo"
    )


def test_check_global_allow_true():
    """Test global_allow set to True."""
    configurator = Configurator(
        template="bobtemplates.plone:content_type",
        target_directory="collective.foo.bar",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "dexterity_type_global_allow": "y",
        },
    )
    with pytest.raises(SkipQuestion):
        content_type.check_global_allow(configurator, None)


def test_check_global_allow_false():
    """Test global_allow set to False."""
    configurator = Configurator(
        template="bobtemplates.plone:content_type",
        target_directory="collective.foo.bar",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "dexterity_type_global_allow": "f",
            "dexterity_parent_container_type_name": "Folder",
        },
    )
    with pytest.raises(SkipQuestion):
        content_type.check_global_allow(configurator, None)


def test_update_parent_types_fti_xml(tmpdir):
    """Test xml changes when changes are already in place."""
    target_path = tmpdir.strpath + "/collective.sample"
    package_path = target_path + "/src/collective/sample"
    profiles_path = package_path + "/profiles/default/types"
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(profiles_path)
    template = """<?xml version="1.0"?>
<object xmlns:i18n="http://xml.zope.org/namespaces/i18n"
    name="My Parent"
    meta_type="Dexterity FTI"
    i18n:domain="collective.sample">
  <property name="global_allow">True</property>
  <property name="filter_content_types">True</property>
  <property name="allowed_content_types">
    <element value="child" />
  </property>
</object>
"""
    with open(os.path.join(profiles_path + "/My_Parent.xml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:content_type",
        target_directory="collective.sample",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "dexterity_type_name": "child",
            "dexterity_type_global_allow": "f",
            "dexterity_parent_container_type_name": "My Parent",
        },
    )
    configurator.variables["package_folder"] = package_path
    content_type._update_parent_types_fti_xml(configurator)

    with open(os.path.join(profiles_path + "/My_Parent.xml")) as f:
        content = f.read()
        if content != template:
            pytest.raises(ValidationError)


def test_update_rolemap_xml(tmpdir):
    """Test rolemap.xml changes when changes are already in place."""
    target_path = tmpdir.strpath + "/collective.sample"
    package_path = target_path + "/src/collective/sample"
    profiles_path = package_path + "/profiles/default"
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(profiles_path)
    template = """<?xml version="1.0"?>
<rolemap>
  <permissions>
  <!-- -*- extra stuff goes here -*- -->

    <permission name="collective.sample: Add Parent" acquire="True">
      <role name="Manager"/>
      <role name="Site Administrator"/>
      <role name="Owner"/>
      <role name="Contributor"/>
    </permission>
  </permissions>
</rolemap>
"""
    with open(os.path.join(profiles_path + "/rolemap.xml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:content_type",
        target_directory="collective.sample",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "dexterity_type_name": "parent",
        },
    )
    configurator.variables["package_folder"] = package_path
    configurator.variables["package.dottedname"] = "bobtemplates.plone"
    configurator.variables["dexterity_type_name_klass"] = "Parent"
    content_type._update_rolemap_xml(configurator)

    with open(os.path.join(profiles_path + "/rolemap.xml")) as f:
        content = f.read()
        if content != template:
            pytest.raises(ValidationError)


def test_update_permissions_zcml(tmpdir):
    """Test zcml changes when changes are already in place."""
    target_path = tmpdir.strpath + "/collective.sample"
    package_path = target_path + "/src/collective/sample"
    os.makedirs(target_path)
    os.makedirs(package_path)
    template = """<configure
  xmlns="http://namespaces.zope.org/zope"
  xmlns:zcml="http://namespaces.zope.org/zcml"
  i18n_domain="plone">
  <configure zcml:condition="installed AccessControl.security">
  <!-- -*- extra stuff goes here -*- -->
    <permission
        id="collective.sample.AddParent"
        title="collective.sample: Add Parent"
    />
  </configure>
</configure>
"""
    with open(os.path.join(package_path + "/permissions.zcml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:content_type",
        target_directory="collective.sample",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "dexterity_type_name": "parent",
        },
    )
    configurator.variables["package_folder"] = package_path
    configurator.variables["package.dottedname"] = "bobtemplates.plone"
    configurator.variables["dexterity_type_name_klass"] = "Parent"
    content_type._update_permissions_zcml(configurator)

    with open(os.path.join(package_path + "/permissions.zcml")) as f:
        content = f.read()
        if content != template:
            pytest.raises(ValidationError)


def test_post_renderer(tmpdir):
    """Test post rendering."""
    target_dir = tmpdir.strpath + "/collective.foo"
    package_path = target_dir + "/src/collective/foo"
    profiles_path = package_path + "/profiles/default"
    os.makedirs(target_dir)
    os.makedirs(package_path)
    os.makedirs(profiles_path + "/types")

    template = SETUPPY_TEMPLATE
    with open(os.path.join(target_dir + "/setup.py"), "w") as f:
        f.write(template)

    template = """<?xml version="1.0" encoding="UTF-8"?>
<metadata>
  <version>1000</version>
  <dependencies>

  </dependencies>
</metadata>
"""
    with open(os.path.join(profiles_path + "/metadata.xml"), "w") as f:
        f.write(template)

    template = """<?xml version="1.0"?>
<rolemap>
  <permissions>
  <!-- -*- extra stuff goes here -*- -->

  </permissions>
</rolemap>
"""
    with open(os.path.join(profiles_path + "/rolemap.xml"), "w") as f:
        f.write(template)

    template = """<?xml version="1.0"?>
<object name="portal_types" meta_type="Plone Types Tool">
 <property name="title">Controls the available contenttypes in your portal
 </property>
 <!--<object name="example_ct" meta_type="Dexterity FTI"/>-->
</object>
"""
    with open(os.path.join(profiles_path + "/types.xml"), "w") as f:
        f.write(template)

    template = """<configure
  xmlns="http://namespaces.zope.org/zope"
  xmlns:zcml="http://namespaces.zope.org/zcml"
  i18n_domain="plone">

  <configure zcml:condition="installed AccessControl.security">
  <!-- -*- extra stuff goes here -*- -->


  </configure>

</configure>
"""
    with open(os.path.join(package_path + "/permissions.zcml"), "w") as f:
        f.write(template)

    template = """
[main]
version=5.1
"""
    with open(os.path.join(target_dir + "/bobtemplate.cfg"), "w") as f:
        f.write(template)

    configurator = Configurator(
        template="bobtemplates.plone:addon",
        target_directory=package_path,
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "dexterity_type_name": "Task",
            "plone.version": "5.1",
        },
    )

    os.chdir(package_path)
    base.set_global_vars(configurator)
    content_type.prepare_renderer(configurator)
    content_type.post_renderer(configurator)
