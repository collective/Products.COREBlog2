# coding=utf-8

from Products.CMFCore.utils import getToolByName
from Products.CMFFormController.FormAction import FormActionKey
from Products.Archetypes.Extensions.utils import installTypes
from Products.Archetypes.Extensions.utils import install_subskin
from Products.Archetypes.public import listTypes

from Acquisition import aq_base

from StringIO import StringIO

from Products.CMFDynamicViewFTI.migrate import migrateFTIs

from Products.COREBlog2.config import *
from Products.COREBlog2.COREBlogTool import COREBlog2Tool

def install(self):
    """Install COREBlog2: Install content types, skin layer, install the
    stylesheet, set up global properties, enable the portal factory and
    set up form controller actions for the widget actions
    """

    out = StringIO()

    # Install tool
    id = COREBlog2Tool.id
    if not hasattr(aq_base(self), id):
        addTool = self.manage_addProduct['COREBlog2'].manage_addTool
        addTool(COREBlog2Tool.meta_type)
        print >>out, 'Installing COREBlog2 Tool'
        

    print >> out, "Installing COREBlog2"

    # Install types
    classes = listTypes(PROJECTNAME)
    installTypes(self, out,
                 classes,
                 PROJECTNAME)
    print >> out, "Installed types"

    # Install skin
    install_subskin(self, out, GLOBALS)
    print >> out, "Installed skin"

    # Migrate FTI, to make sure we get the necessary infrastructure for the
    # 'display' menu to work.
    try:
        migrated = migrateFTIs(self, product=PROJECTNAME)
        print >>out, "Switched to DynamicViewFTI: %s" % ', '.join(migrated)
    except:
        print >>out, "DynamicViewFTI might not works well. You use Plone 3.0 alpha ?"

    # Enable portal_factory
    factory = getToolByName(self, 'portal_factory')
    types = factory.getFactoryTypes().keys()
    for add_type in ['COREBlog2','COREBlogEntry','COREBlogCategory']:
        if add_type not in types:
            types.append(add_type)
            factory.manage_setPortalFactoryTypes(listOfTypeIds = types)

    print >> out, "Added COREBlog2 to portal_factory"

    #propsTool = getToolByName(self, 'portal_properties')
    #siteProperties = getattr(propsTool, 'site_properties')
    #navtreeProperties = getattr(propsTool, 'navtree_properties')

    # install enabled index for topic
    atcttool = getToolByName(self, 'portal_atct')
    atcttool.addIndex('getTags', 'Tag', 'Tag(Category)', True, 
                      ('ATListCriterion', ))

    return out.getvalue()