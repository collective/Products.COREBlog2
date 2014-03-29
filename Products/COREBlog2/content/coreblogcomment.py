##############################################################################
#
# coreblogcomment.py
# Class for COREBlog2 Comment
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
#$Id: coreblogcomment.py 225 2007-03-31 14:22:33Z ats $
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


COREBlogCommentSchema = ATContentTypeSchema.copy() +  Schema((

    #Comment content data
    StringField('author',
        searchable=True,
        widget=StringWidget(label='Author',
            description='',
            label_msgid="label_coreblog_comment_author",
            description_msgid="help_coreblog_comment_author",
            i18n_domain="plone",
            size=60),
        ),

    StringField('email',
        searchable=True,
        widget=StringWidget(label='email',
            description='',
            label_msgid="label_coreblog_comment_email",
            description_msgid="help_coreblog_comment_email",
            i18n_domain="plone",
            size=60),
        ),

    StringField('url',
        searchable=True,
        widget=StringWidget(label='url',
            description='',
            label_msgid="label_coreblog_comment_url",
            description_msgid="help_coreblog_comment_url",
            i18n_domain="plone",
            size=60),
        ),

    TextField('body',
        searchable=True,
        primary=True,
        index='TextIndex',
        default_output_type='text/html',
        default_content_type='text/plain',
        widget=TextAreaWidget(label='Body',
            description='',
            label_msgid="label_coreblog_comment_body",
            description_msgid="help_coreblog_comment_body",
            i18n_domain="plone",
            cols=40,rows=5),
        ),

    StringField('post_ip',
        searchable=True,
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

finalizeATCTSchema(COREBlogCommentSchema)

class COREBlogComment(ATCTContent):
    """
    This is a Category class for COREBlog2
    """
    
    schema = COREBlogCommentSchema
    archetype_name = "COREBlog Comment"
    meta_type = 'COREBlogComment'

    security = ClassSecurityInfo()
    security.declareObjectProtected(View)
    
    #_at_rename_after_creation = True
    
    # Not to be shown at navigation
    exclude_from_nav = True

    aliases = updateAliases(base_aliases,
        {
        'view' : 'cbcomment_view',
        'edit' : 'cbcomment_edit'
        })

    security.declareProtected(View, 'getParentEntry')
    def getParentEntry(self):
        entry = self.getBRefs()
        if entry:
            return entry[0]



registerType(COREBlogComment, PROJECTNAME)
