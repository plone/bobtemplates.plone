class RegEntry:
    def __init__(self):
        self.template = ""
        self.plonecli_alias = ""
        self.depend_on = None
        self.deprecated = False
        self.info = ""


# def plone_addon():
#     reg = RegEntry()
#     reg.template = "bobtemplates.plone:addon"
#     reg.plonecli_alias = "addon"
#     return reg


def plone_buildout():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:buildout"
    reg.plonecli_alias = "buildout"
    return reg


def plone_theme():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:theme"
    reg.plonecli_alias = "theme"
    return reg


def plone_theme_barceloneta():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:theme_barceloneta"
    reg.plonecli_alias = "theme_barceloneta"
    return reg


def plone_theme_basic():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:theme_basic"
    reg.plonecli_alias = "theme_basic"
    return reg


def plone_content_type():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:content_type"
    reg.plonecli_alias = "content_type"
    return reg


def plone_view():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:view"
    reg.plonecli_alias = "view"
    return reg


def plone_portlet():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:portlet"
    reg.plonecli_alias = "portlet"
    return reg


def plone_viewlet():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:viewlet"
    reg.plonecli_alias = "viewlet"
    return reg


def plone_vocabulary():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:vocabulary"
    reg.plonecli_alias = "vocabulary"
    return reg


def plone_behavior():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:behavior"
    reg.plonecli_alias = "behavior"
    return reg


def plone_restapi_service():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:restapi_service"
    reg.plonecli_alias = "restapi_service"
    return reg


def plone_svelte_app():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:svelte_app"
    reg.plonecli_alias = "svelte_app"
    return reg


def plone_subscriber():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:subscriber"
    reg.plonecli_alias = "subscriber"
    return reg


def plone_indexer():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:indexer"
    reg.plonecli_alias = "indexer"
    return reg


def plone_upgrade_step():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:upgrade_step"
    reg.plonecli_alias = "upgrade_step"
    return reg


def plone_controlpanel():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:controlpanel"
    reg.plonecli_alias = "controlpanel"
    return reg


def plone_mockup_pattern():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:mockup_pattern"
    reg.plonecli_alias = "mockup_pattern"
    return reg


def plone_form():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:form"
    reg.plonecli_alias = "form"
    return reg


def plone_site_initialization():
    reg = RegEntry()
    reg.template = "bobtemplates.plone:site_initialization"
    reg.plonecli_alias = "site_initialization"
    return reg
