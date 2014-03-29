##############################################################################
#
# COREBlogCategory.py
# Class for COREBlog2 Category
#
# Copyright (c) 2005 Atsushi Shibata(shibata@webcore.co.jp).
#                                       All Rights Reserved.
#
# Additional imprementation to change superclass to ATCTFolder
#  by Ben <ben [at] smoothify.com> (thanks a lot!)
#
# Permission to use, copy, modify, and distribute this software and its 
# documentation for any purpose and without fee is hereby granted, provided that
# the above copyright notice appear in all copies and that both that copyright 
# notice and this permission notice appear in supporting documentation, and that
# the name of Atsushi Shibata not be used in advertising or publicity pertaining 
# to distribution of the software without specific, written prior permission. 
# 
# ATSUSHI SHIBAT DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, 
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
# EVENT SHALL SHIBAT ATSUSHI BE LIABLE FOR ANY SPECIAL, INDIRECT OR 
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
# USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE. 
#
#$Id: coreblogcategory.py 335 2007-09-06 03:38:30Z ats $
#
##############################################################################

#Base classes
from Products.ATContentTypes.content.base import ATCTContent,ATCTFolder
from Products.ATContentTypes.content.schemata import ATContentTypeSchema,\
                                                     finalizeATCTSchema
from Products.ATContentTypes.interfaces import IATFolder
from Products.Archetypes.public import Schema,registerType
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
#Fields
from Products.Archetypes.public import StringField,ImageField,IntegerField
#Widgets
from Products.Archetypes.public import StringWidget,TextAreaWidget,\
                                       ImageWidget,IntegerWidget

from Products.Archetypes.Marshall import PrimaryFieldMarshaller
from Products.COREBlog2.config import PROJECTNAME

#Interfaces
#from Products.CMFPlone.interfaces.NonStructuralFolder import \
#                                                    INonStructuralFolder

from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import View,ModifyPortalContent
from Products.CMFCore.utils import getToolByName

from zope.interface import implements
from actions_proxy import updateAliases, base_aliases

COREBlogCategorySchema = ATContentTypeSchema.copy() +  Schema((

    IntegerField('internal_id',
        searchable=False,
        isMetadata=True,
        mutator="setInternal_id",
        widget=IntegerWidget(label='Internal ID',
            description='',
            visible={'view':'invisible','edit':'hidden'},
            ),
        ),

    ImageField('category_image',
        widget=ImageWidget(label='Category image',
            description='',
            label_msgid='label_category_image',
            description_msgid='help_category_image',
            i18n_domain='plone',
            ),
        sizes={ 'icon':(16,16)},
        ),

    ),
    marshall=PrimaryFieldMarshaller(),
    )

finalizeATCTSchema(COREBlogCategorySchema)

class COREBlogCategory(ATCTFolder):
    """
    Category class for coreblog2
    """
    
    schema = COREBlogCategorySchema
    meta_type = 'COREBlogCategory'
    typeDescMsgId  = 'coreblog2_description_coreblog2category'

    implements(IATFolder) # INonStructuralFolder

    # Not to be shown at add item menu
    global_allow = False
    
    security = ClassSecurityInfo()
    security.declareObjectProtected(View)
    
    _at_rename_after_creation = True
    
    aliases = updateAliases(base_aliases,
        {
        'view' : 'cbcategory_view',
        'edit' : 'cbcategory_edit'
        })

    # Not to be shown at navigation
    exclude_from_nav = True

    def canSetDefaultPage(self):
        return False

    # Override initializeArchetype to turn on syndication by default
    def initializeArchetype(self, **kwargs):
        self.allow_discussion = False
        ret_val = ATCTFolder.initializeArchetype(self, **kwargs)
        # Enable topic syndication by default
        syn_tool = getToolByName(self, 'portal_syndication', None)
        if syn_tool is not None:
            if (syn_tool.isSiteSyndicationAllowed() and \
                    not syn_tool.isSyndicationAllowed(self)):
                syn_tool.enableSyndication(self)
        return ret_val

    security.declareProtected(ModifyPortalContent, 'setInternal_id')
    def setInternal_id(self, value):
        if not self.getInternal_id():
            self.Schema()['internal_id'].set(self,value)

    security.declarePrivate('synContentValues')
    def synContentValues(self):
        """Getter for syndacation support
        """
        syn_tool = getToolByName(self, 'portal_syndication')
        limit = int(syn_tool.getMaxItems(self))

        brains =  self.getEntryInCategory(\
                    category_ids = [self.getInternal_id()],
                    batch=True,
                    sort_order='reverse',
                    b_size=limit,b_start= 0,full_objects=False)

        objs = [brain.getObject() for brain in brains]
        return [obj for obj in objs if obj is not None]

    security.declarePrivate('manage_afterAdd')
    def manage_afterAdd(self, item, container):
        # Do internal ID management
        # Find out max category ID

        if not self.getInternal_id():
            a_id = 0
            for cat in container.objectValues([self.meta_type]):
                try:
                    a_id = max(cat.getInternal_id(),a_id)
                except:
                    pass
            self.setInternal_id(a_id + 1)

        #Call base class initialize method
        ATCTFolder.manage_afterAdd(self, item, container)


registerType(COREBlogCategory, PROJECTNAME)
