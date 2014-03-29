##############################################################################
#
# coreblogstufffolder.py
# Classes for COREBlog2 Folder for Comments/Trackbacks - Categories
#
# Copyright (c) 2005 Atsushi Shibata(shibata@webcore.co.jp).
#                                       All Rights Reserved.
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
#$Id: coreblogstufffolder.py 225 2007-03-31 14:22:33Z ats $
#
##############################################################################

#Base classes
from Products.ATContentTypes.content.base import ATCTBTreeFolder,ATCTFolder
from plone.app.folder.folder import ATFolder
from plone.app.folder.folder import ATFolderSchema
from Products.ATContentTypes.content.folder import ATBTreeFolder,\
                             ATBTreeFolderSchema,\
                             finalizeATCTSchema
from Products.ATContentTypes.interfaces import IATBTreeFolder,IATFolder
from Products.Archetypes.public import Schema,registerType
from Products.ATContentTypes.interface import IATFolder

#Fields
from Products.Archetypes.public import StringField,IntegerField,\
                                       LinesField,ReferenceField
#Widgets
from Products.Archetypes.public import StringWidget,TextAreaWidget,\
                                       IntegerWidget,SelectionWidget

from Products.Archetypes.utils import DisplayList
from Products.Archetypes.Marshall import PrimaryFieldMarshaller
from Products.CMFCore import permissions as CMFCorePermissions
from Products.COREBlog2.config import PROJECTNAME

from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import View

from actions_proxy import updateAliases, base_aliases
from zope.interface import implements

__author__  = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'

COREBlogCommentFolderSchema = ATBTreeFolder.schema.copy()
COREBlogCategoryFolderSchema = ATBTreeFolder.schema.copy()

#Finalize schema definition
finalizeATCTSchema(COREBlogCommentFolderSchema)
finalizeATCTSchema(COREBlogCategoryFolderSchema)


class COREBlogCommentFolder(ATBTreeFolder):
    """
    This is a COREBlogCommentFolder class
    """
    
    archetype_name = "COREBlog Comment Folder"
    meta_type = 'COREBlogCommentFolder'
    
    exclude_from_nav = True
    suppl_views    = ()
    
    security = ClassSecurityInfo()
    security.declareObjectProtected(View)
    
    implements(IATBTreeFolder)
    
    aliases = updateAliases(base_aliases,
        {
        'view' : 'cbcommentfolder_view',
        })

    def canSetDefaultPage(self):
        return False

registerType(COREBlogCommentFolder, PROJECTNAME)

class COREBlogCategoryFolder(ATFolder):
    """
    This is a COREBlogCategoryFolder class
    """
    
    archetype_name = "COREBlog Category Folder"
    meta_type = 'COREBlogCategoryFolder'
    
    exclude_from_nav = True
    suppl_views    = ()
    
    security = ClassSecurityInfo()
    security.declareObjectProtected(View)
    
    implements(IATFolder)
    
    def canSetDefaultPage(self):
        return False

registerType(COREBlogCategoryFolder, PROJECTNAME)

