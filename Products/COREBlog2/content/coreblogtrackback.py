##############################################################################
#
# coreblogtrackback.py
# Class for COREBlog2 Trackback
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
#$Id: coreblogtrackback.py 225 2007-03-31 14:22:33Z ats $
#
##############################################################################

#Base classes
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema,\
                                                     finalizeATCTSchema
from Products.ATContentTypes.interfaces import IATBTreeFolder
from Products.Archetypes.public import Schema,registerType
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
#Fields
from Products.Archetypes.public import StringField,TextField,IntegerField
#Widgets
from Products.Archetypes.public import StringWidget,TextAreaWidget,IntegerWidget
#Marshaller
from Products.Archetypes.public import RFC822Marshaller

from Products.Archetypes.public import BaseSchema, Schema
from Products.Archetypes.public import StringField,IntegerField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import BaseContent, registerType
from Products.Archetypes.Marshall import PrimaryFieldMarshaller
from Products.CMFCore import permissions as CMFCorePermissions
from Products.COREBlog2.config import PROJECTNAME

from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import View

from actions_proxy import updateAliases, base_aliases

COREBlogTrackbackSchema = ATContentTypeSchema.copy() +  Schema((

    #Comment content data
    StringField('url',
        searchable=1,
        widget=StringWidget(label='URL',
            description='',
            label_msgid="label_coreblog_trackback_url",
            description_msgid="help_coreblog_trackback_url",
            i18n_domain="plone",
            size=60),
        ),

    StringField('excerpt',
        searchable=1,
        primary=True,
        index='TextIndex',
        default_output_type='text/html',
        default_content_type='text/html',
        widget=StringWidget(label='excerpt',
            description='',
            label_msgid="label_coreblog_trackback_excerpt",
            description_msgid="help_coreblog_trackback_excerpt",
            i18n_domain="plone",
            size=60),
        ),

    StringField('blog_name',
        searchable=1,
        widget=StringWidget(label='blog_name',
            description='',
            label_msgid="label_coreblog_trackback_blog_name",
            description_msgid="help_coreblog_trackback_blog_name",
            i18n_domain="plone",
            size=60),
        ),

    StringField('post_ip',
        searchable=1,
        index='FieldIndex',
        widget=StringWidget(label='IP',
            description='',
            label_msgid="label_coreblog_comment_post_ip",
            description_msgid="help_coreblog_comment_post_ip",
            i18n_domain="plone",
            size=60),
        ),


    ),
    marshall=RFC822Marshaller(),
    )

finalizeATCTSchema(COREBlogTrackbackSchema)

class COREBlogTrackback(ATCTContent):
    """
    This is a Category class for COREBlog2
    """
    
    schema = COREBlogTrackbackSchema
    archetype_name = "COREBlog Trackback"
    meta_type = 'COREBlogTrackback'

    security = ClassSecurityInfo()
    security.declareObjectProtected(View)
    
    _at_rename_after_creation = True
    
    aliases = updateAliases(base_aliases,
        {
        'view' : 'cbtrackback_view',
        'edit' : 'cbtrackback_edit'
        })

    # Not to be shown at navigation
    exclude_from_nav = True

    security.declareProtected(View, 'getParentEntry')
    def getParentEntry(self):
        entry = self.getBRefs()
        if entry:
            return entry[0]

registerType(COREBlogTrackback, PROJECTNAME)
