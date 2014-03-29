##############################################################################
#
# coreblogentry.py
# Class for COREBlog2 Entry
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
#$Id: coreblogentry.py 335 2007-09-06 03:38:30Z ats $
#
##############################################################################

#Base classes
from Products.ATContentTypes.content.base import ATCTContent,\
                 translateMimetypeAlias
from Products.ATContentTypes.content.schemata import ATContentTypeSchema,\
                                                     finalizeATCTSchema
from Products.ATContentTypes.interfaces import IATBTreeFolder
from Products.Archetypes.public import Schema,registerType
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.ATContentTypes.interfaces import IHistoryAware

from Products.ATContentTypes.interfaces import IATDocument
from Products.ATContentTypes.interfaces import IATContentType
#Fields
from Products.Archetypes.public import StringField,TextField,IntegerField,\
                                       ReferenceField,LinesField
#Widgets
from Products.Archetypes.public import StringWidget,TextAreaWidget,\
                                       IntegerWidget,RichWidget,\
                                       ReferenceWidget,SelectionWidget,\
                                       IdWidget
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget \
                                            import ReferenceBrowserWidget

from Products.Archetypes.utils import IntDisplayList, DisplayList
from Products.Archetypes.public import AnnotationStorage
#Marshaller
from Products.Archetypes.public import RFC822Marshaller
#Custom widget
from Products.COREBlog2.COREBlogWidgets import CategoryWidget

from Products.Archetypes.public import BaseSchema, Schema
from Products.Archetypes.public import StringField,IntegerField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import BaseContent, registerType
from Products.Archetypes.Marshall import PrimaryFieldMarshaller
from Products.CMFCore import permissions as CMFCorePermissions
from Products.CMFCore.utils import getToolByName
from Products.COREBlog2.config import PROJECTNAME,\
                  comemnt_rel_id,trackback_rel_id,\
                  coreblogentry_meta_type,coreblogcomment_meta_type,\
                  coreblogtrackback_meta_type

from Products.COREBlog2.configuration import zconf

from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import View,ModifyPortalContent

from actions_proxy import updateAliases, updateActions, \
                          base_actions, base_aliases
from zope.interface import implements

from sets import Set
from types import *

description_length = zconf.coreblog2.description_length

comment_status = (  (1, "None(cannot add,hidden)",
                                "label_entrycommentstatus_none"),
                    (2, "Open(can add,shown)",
                                "label_entrycommentstatus_open"),
                    (3, "Closed(cannot add,shown)",
                                "label_entrycommentstatus_closed"),
                    )

trackback_status = ((1, "None(cannot add,hidden)",
                         "label_entrycommentstatus_none"),
                    (2, "Open(can add,shown)",
                        "label_entrycommentstatus_open"),
                    (3, "Closed(cannot add,shown)",
                        "label_entrycommentstatus_closed"),
                    )

entryschema = ATContentTypeSchema.copy()

entryschema['relatedItems'].widget = ReferenceBrowserWidget(
            allow_search = True,
            allow_browse = True,
            show_indexes = False,
            force_close_on_insert = True,
            image_method = 'image_icon',

            label = "Related Item(s)",
            label_msgid = "label_related_items",
            description = "",
            description_msgid = "help_related_items",
            i18n_domain = "plone",
            visible = {'edit' : 'visible', 'view' : 'invisible' }
            )



COREBlogEntrySchema = entryschema + Schema((

    StringField('id',
        required=True,
        widget=IdWidget(label='ID',
            description='',
            label_msgid='label_entry_id',
            description_msgid='help_entry_id',
            i18n_domain='plone',
            size=60),
        ),

    #Entry contents
    StringField('subtitle',
        searchable=True,
        index='TextIndex',
        widget=StringWidget(label='Subtitle',
            description='',
            label_msgid='label_subtitle',
            description_msgid='help_subtitle',
            i18n_domain='plone',
            size=60),
        ),

    TextField('body',
        required=True,
        primary=True,
        searchable=True,
        index='TextIndex',
        default_output_type='text/html',
        default_content_type='text/html',
        allowable_content_types = zconf.coreblog2.allowed_content_types ,
        widget=RichWidget(label='Body',
            description='',
            label_msgid='label_body',
            description_msgid='help_body',
            i18n_domain='plone',
            allow_file_upload=False,
            cols=40,rows=30),
        ),

    TextField('extend',
        searchable=True,
        index='TextIndex',
        default_output_type='text/html',
        default_content_type='text/html',
        allowable_content_types = zconf.coreblog2.allowed_content_types ,
        widget=RichWidget(label='Extend',
            description='',
            label_msgid='label_extend',
            description_msgid='help_extend',
            i18n_domain='plone',
            allow_file_upload=False,
            cols=40,rows=5),
        schemata='cbentry_extented_fields',
        ),

    #Category
    LinesField('entry_categories',
        required=True,
        widget=CategoryWidget(label='Category(s)',
            description='',
            label_msgid='label_entry_categories',
            description_msgid='help_entry_categories',
            i18n_domain='plone',),
       index='KeywordIndex',
        ),

    LinesField('tags',
        required=False,
        widget=CategoryWidget(label='Tag(s)',
            description='',
            label_msgid='label_entry_categories',
            description_msgid='help_entry_categories',
            i18n_domain='plone',
            visible={'edit':False,'view':False},
            ),
       index='KeywordIndex',
        ),

    #Comments
    ReferenceField('entry_comments',
        multivalued=True,
        relationship=comemnt_rel_id,
        allowed_types=(coreblogcomment_meta_type,),
        widget=ReferenceWidget(label='Comment references',
            label_msgid='label_entry_comments',
            description_msgid='help_entry_comments',
            visible={'view':'invisible','edit':'hidden'},
            i18n_domain='plone',),
        ),

    #Trackbacks
    ReferenceField('entry_trackbacks',
        multivalued=True,
        relationship=trackback_rel_id,
        allowed_types=(coreblogtrackback_meta_type,),
        ),

    TextField('trackback_url',
        searchable=0,
        default_output_type='text/plain',
        widget=TextAreaWidget(label='Trackback',
            description='',
            label_msgid='label_trackback',
            description_msgid='help_trackback',
            i18n_domain='plone',
            allow_file_upload=False,
            #visible={'view':'invisible','edit':'hidden'},
            cols=40,rows=3),
        ),

    TextField('sent_trackback_url',
        searchable=False,
        default_output_type='text/plain',
        ),

    IntegerField('allow_comment',
        searchable=0,
        default = 2,
        widget=SelectionWidget(label='Comment status',
            label_msgid='label_allow_comment',
            description_msgid='help_allow_comment',
            i18n_domain='plone',),
        vocabulary=IntDisplayList(comment_status),
        schemata='cbentry_extented_fields',
        ),

    IntegerField('receive_trackback',
        searchable=0,
        default = 2,
        widget=SelectionWidget(label='Trackback status',
            label_msgid='label_receive_trackback',
            description_msgid='help_receive_trackback',
            i18n_domain='plone',),
        vocabulary=IntDisplayList(trackback_status),
        schemata='cbentry_extented_fields',
        ),

    IntegerField('media_position',
        searchable=0,
        default = 1,
        widget=SelectionWidget(label='Media position',
                    description='',
                    label_msgid='label_media_position',
                    description_msgid='help_media_position',
                    i18n_domain='plone',),
        vocabulary=IntDisplayList((
                  (1, "Top,horizontal",
                      "label_media_position_top"),
                  (2, "Bottom,horizontal",
                      "label_media_position_bottom"),
                  (3, "Left,vertical",
                      "label_media_position_left"),
                  (4, "Right,vertical",
                      "label_media_position_right"),
                    ))
        ),

    StringField('media_size',
        searchable=0,
        default = 'thumb',
        widget=SelectionWidget(label='Media size',
                    description='',
                    label_msgid='label_media_size',
                    description_msgid='help_media_size',
                    i18n_domain='plone',),
        vocabulary=DisplayList((
                    ('large', "Large (768,768)",
                        "label_media_size_large"),
                    ('preview', "Prenew (400,400)",
                        "label_media_size_preview"),
                    ('mini', "Mini (200,200)",
                        "label_media_size_mini"),
                    ('thumb', "Thumbnail (128,128)",
                        "label_media_size_thumbnail"),
                    ('no_resize', "No resize",
                        "label_media_size_noresize"),
                    ))
        ),

    ), marshall=RFC822Marshaller()
    )

finalizeATCTSchema(COREBlogEntrySchema)

class COREBlogEntry(ATCTContent):
    """
    This is an Entry class for coreblog2
    """
    
    schema = COREBlogEntrySchema
    archetype_name = "COREBlog Entry"
    meta_type = coreblogentry_meta_type
    # Not to be shown at add item menu
    global_allow = False
    allow_discussion = False
    
    implements(IATContentType, IATDocument, IHistoryAware)
    
    security = ClassSecurityInfo()
    security.declareObjectProtected(View)

    _at_rename_after_creation = True

    actions = updateActions(base_actions ,(
        {
        'id': 'comments',
        'name': 'Comments',
        'action': 'string:${object_url}/cbentry_comments',
        'permissions': (CMFCorePermissions.ModifyPortalContent,),
        },
        {
        'id': 'trackbacks',
        'name': 'Trackbacks',
        'action': 'string:${object_url}/cbentry_trackbacks',
        'permissions': (CMFCorePermissions.ModifyPortalContent,),
        },
            ))

    aliases = updateAliases(base_aliases,
        {
        'edit' : 'cbentry_edit',
        'view' : 'cbentry_view'
        })

    # Not to be shown at navigation
    exclude_from_nav = True

    # Constants
    comment_none = 1
    comment_open = 2
    comment_closed = 3

    trackback_none = 1
    trackback_open = 2
    trackback_closed = 3


    def initializeArchetype(self, **kwargs):
        self.allow_discussion = False
        ATCTContent.initializeArchetype(self, **kwargs)
        self._ping_sent = False
        # manage index

    security.declarePrivate('manage_beforeDelete')
    def manage_beforeDelete(self, item, container):
        #
        # Hook method, called before object deletion
        #

        # Get list for ids of referenced comments,trackbacks
        ids = [obj.id for obj in self.getComment()]
        ids += [obj.id for obj in self.getTrackback()]

        # Now delete them all!
        self.aq_parent.getCommentFolder().manage_delObjects(ids)

        # Call superclass method
        ATCTContent.manage_beforeDelete(self,item, container)


    security.declareProtected(ModifyPortalContent, 'setBody')
    def setBody(self, value, **kwargs):
        #
        # The setter for body, also making copy to 'description',
        # and store 'flat_descriptin' for trackback auto discoverty
        #
        self.getField('body').set(self, value, **kwargs)
        transformer = getToolByName(self,'portal_transforms')
        flat_desc =  transformer.convertToData('text/plain',self.getBody())
        orig_len = len(flat_desc)
        if type(flat_desc) != UnicodeType:
            flat_desc = unicode(flat_desc,'utf-8','ignore')
        flat_desc = flat_desc[:description_length].encode('utf-8')
        flat_desc = flat_desc.replace('\n','')
        flat_desc = flat_desc.replace('\r','')
        if orig_len > description_length:
            flat_desc += '...'
        self.setDescription(flat_desc)

    #
    # Codes for CMF compatibility
    #

    security.declareProtected(View, 'CookedBody')
    def CookedBody(self, stx_level='ignored'):
        """
        Method for CMF compatibility, returns rendered body
        """
        return self.getBody()


    security.declareProtected(ModifyPortalContent, 'EditableBody')
    def EditableBody(self):
        """
        Method for CMF compatibility, returns raw body
        """
        return self.getRawBody()

    security.declareProtected(ModifyPortalContent,
                              'setFormat')
    def setFormat(self, value):
        """
        Method for CMF compatibility, set for body format
        """
        if not value:
            value = 'text/html'
        else:
            value = translateMimetypeAlias(value)
        ATCTContent.setFormat(self, value)


    security.declareProtected(View, 'getObjSize')
    def getObjSize(self):
        return len(self.getBody() + self.getExtend())


    security.declarePrivate('_renameAfterCreation')
    def _renameAfterCreation(self, check_auto_id=False):
        """
        Renames an object like its normalized title.
        Overridden method
        """

        if check_auto_id and not self._isIDAutoGenerated(self.getId()):
            # No auto generated id
            return False

        # Check if hook method is there
        if hasattr(self,'getEntryId'):
            new_id = self.getEntryId()
        if new_id:
            invalid_id = False
            check_id = getattr(self, 'check_id', None)
            if check_id is not None:
                invalid_id = check_id(new_id, required=1)
            else:
                # If check_id is not available just look for conflicting ids
                parent = aq_parent(aq_inner(self))
                invalid_id = new_id in parent.objectIds()

            if not invalid_id:
                # Can't rename without a subtransaction commit when using
                # portal_factory!
                get_transaction().commit(1)
                self.setId(new_id)
                return new_id

        return BaseContent._renameAfterCreation(self, check_auto_id)

    #
    # category/tag management
    #

    def _setTags(self, categories):
        try:
            catd = self.aq_parent.getCategoryMap()
            tags = [ catd.get(x, '').get('title', '') for x in categories]
            self.getField('tags').set(self, tags)
        except:
            pass


    security.declareProtected(ModifyPortalContent, 'setEntry_categories')
    def setEntry_categories(self, value, **kwargs):
        #
        # The setter for category, also set values for tags,
        #
        self.getField('entry_categories').set(self, value, **kwargs)
        self._setTags(value)


    security.declareProtected(ModifyPortalContent, 'getTags')
    def getTags(self):
        value = self.getField('tags').get(self)
        if value:
            return value
        else:
            tags = self.getEntry_categories()
            value = self._setTags(tags)
            return value

    #
    # Accessor to prev. next entry
    #

    security.declareProtected(View, 'getNextEntry')
    def getNextEntry(self,full_objects=True):
        """ """
        #
        # Returns next entry, according to date
        #
        parent = self.aq_parent.getCommentFolder()
        ent_list = parent.getNearestEntry(sort_order='normal',\
                        base_date=self.Date(),full_objects=full_objects)
        if len(ent_list) > 1:
            return ent_list[1]
        return None

    security.declareProtected(View, 'getPreviousEntry')
    def getPreviousEntry(self,full_objects=True):
        """ """
        #
        # Returns previous entry, according to date
        #
        parent = self.aq_parent.getCommentFolder()
        ent_list = parent.getNearestEntry(sort_order='reverse',\
                        base_date=self.Date(),full_objects=full_objects)
        if len(ent_list) > 1:
            return ent_list[1]
        return None

    #
    # Comment Management
    #

    security.declareProtected(View, 'getComment')
    def getComment(self,full_objects=True):
        #Returns entry comments

        #Get refecences comment
        coms = self.getRefs(comemnt_rel_id)
        obj_list = []

        #Set content filter
        path = {}
        path['depth'] = 0
        contentFilter = {'path':path,'portal_type':coreblogcomment_meta_type}
        for com in coms:
            path['query'] = '/'.join(com.getPhysicalPath())
            #Tell catalog if comment will be shown in this context
            for cat_obj in \
                self.queryCatalog(contentFilter,show_all=1):
                if full_objects:
                    #Append comment object itself
                    obj_list.append(cat_obj.getObject())
                else:
                    #Append catalog data
                    obj_list.append(cat_obj)
        if full_objects:
            obj_list.sort(lambda x,y: cmp(x.Date(),y.Date()))
        else:
            obj_list.sort(lambda x,y: cmp(x.Date,y.Date))

        return obj_list

    security.declareProtected(View, 'countComment')
    def countComment(self):
        #Returns entry comment count

        #Get refecences comment
        coms = self.getRefs(comemnt_rel_id)
        cnt = 0

        #Set content filter
        path = {}
        path['depth'] = 0
        contentFilter = {'path':path,'portal_type':coreblogcomment_meta_type}
        for com in coms:
            #Tell catalog if comment will be shown in this context
            path['query'] = \
                '/'.join(com.getPhysicalPath())
            if self.queryCatalog(contentFilter,show_all=False):
                cnt += 1
        return cnt

    security.declareProtected(View, 'addComment2Entry')
    def addComment2Entry(self,author='',email='',url='',title='',
                         body='',post_ip='',id='',REQUEST=None):
        #Add comment and reference to entry
        #Further feature is gurded by Zope Security,
        #so some settings in security tab should be done
        #for anonymous comment or something.

        # Check for comment status
        if self.getAllow_comment() != self.comment_open:
            return None

        type_name=coreblogcomment_meta_type
        parent = self.aq_parent.getCommentFolder()
        # Call factory method to create comment object
        if not id:
            id = parent.generateUniqueId()
        new_id = parent.invokeFactory(id=id, type_name=type_name)
        if new_id is None or new_id == '':
           new_id = id

        # Get new comment object
        com = parent[id]

        if not post_ip and REQUEST and REQUEST.has_key('REMOTE_ADDR'):
            post_ip = REQUEST['REMOTE_ADDR']

        # Set attributes
        com.setAuthor(author)
        com.setEmail(email)
        com.setUrl(url)
        com.setTitle(title)
        com.setBody(body)
        com.setPost_ip(post_ip)
        com.setEffectiveDate('')

        # Make sure to be catalloged
        com.indexObject()

        # Add reference
        self.addReference(com,comemnt_rel_id)
        return new_id


    #
    # PING Management
    #
    security.declareProtected(ModifyPortalContent, 'setBody')
    def setPingStatus(self,state=True):
        self._ping_sent = state

    security.declareProtected(View, 'hasPingSent')
    def hasPingSent(self):
        try:
            return self._ping_sent
        except:
            self._ping_sent = True
        return True


    #
    # Trackback Management(Receiving)
    #

    security.declareProtected(View, 'getTrackback')
    def getTrackback(self,full_objects=True):
        #Get refecences trackback
        tbs = self.getRefs(trackback_rel_id)
        obj_list = []

        #Set content filter
        path = {}
        path['depth'] = 0
        contentFilter = {'path':path,'portal_type':coreblogtrackback_meta_type}
        for tb in tbs:
            path['query'] = \
                '/'.join(tb.getPhysicalPath())
            #Tell catalog if trackback will be shown in this context
            for tb_obj in \
                self.queryCatalog(contentFilter,show_all=1):
                if full_objects:
                    #Append trackback object itself
                    obj_list.append(tb_obj.getObject())
                else:
                    #Append catalog data
                    obj_list.append(tb_obj)
        if full_objects:
            obj_list.sort(lambda x,y: cmp(x.Date(),y.Date()))
        else:
            obj_list.sort(lambda x,y: cmp(x.Date,y.Date))

        return obj_list

    security.declareProtected(View, 'countTrackback')
    def countTrackback(self):
        #Returns entry trackback count

        tbs = self.getRefs(trackback_rel_id)
        cnt = 0
        path = {}
        path['depth'] = 0
        contentFilter = {'path':path}
        for tb in tbs:
            path['query'] = \
                '/'.join(tb.getPhysicalPath())
            if self.queryCatalog(contentFilter,show_all=1):
                cnt += 1
        return cnt

    security.declareProtected(View, 'addTrackback2Entry')
    def addTrackback2Entry(self,title='',url='',blog_name='',
                         excerpt='',post_ip='',id='',REQUEST=None):
        #Add trackback and reference to entry
        #Further feature is gurded by Zope Security,
        #so some settings in security tab should be done
        #for anonymous trackback or something.

        # Check for trackback status
        if self.getReceive_trackback() != self.trackback_open:
            return None

        type_name=coreblogtrackback_meta_type
        parent = self.aq_parent.getCommentFolder()
        # Call factory method to create trackback object
        if not id:
            id = parent.generateUniqueId()
        new_id = parent.invokeFactory(id=id, type_name=type_name)
        if new_id is None or new_id == '':
           new_id = id

        # Get new trackback object
        tb = parent[id]

        if not post_ip and REQUEST and REQUEST.has_key('REMOTE_ADDR'):
            post_ip = REQUEST['REMOTE_ADDR']

        # Set attributes
        tb.setTitle(title)
        tb.setUrl(url)
        tb.setBlog_name(blog_name)
        tb.setExcerpt(excerpt)
        tb.setPost_ip(post_ip)

        # Make sure to be catalloged
        tb.indexObject()

        # Add reference
        self.addReference(tb,trackback_rel_id)
        return new_id


    #
    # Trackback Management(Sending)
    #
    security.declareProtected(ModifyPortalContent, 'getUnsentTrackbacks')
    def getUnsentTrackbacks(self):
        """
        Find if there is unsent trackback, if there, return true.
        """
        tobesent = Set(self.getTrackback_url().split('\n'))
        alreadysent = Set(self.getSent_trackback_url().split('\n'))
        # Get unique unsent trackback url(s)
        unsent = tobesent - alreadysent
        return list(unsent)

    security.declareProtected(ModifyPortalContent, 'sendTrackbacks')
    def sendTrackbacks(self,idx = -1):
        """
        Send trackback.
        If any idx served, only one trackback will be sent.
        If idx == -1, try to send all trackback.
        """
        cbtool = getToolByName(self,'coreblog2_tool')

        tburls = self.getUnsentTrackbacks()
        idxlist = range(0,len(tburls))
        if idx != -1:
            idxlist = [idx]
        senttbs = []
        entry_url = self.absolute_url()
        if self.aq_parent.getTrackback_base():
            repbase = self.aq_parent.absolute_url()
            entry_url = entry_url.replace(repbase,\
                            self.aq_parent.getTrackback_base())

        blog_title = self.aq_parent.title
        rls = []
        successfully_sent = []
        for i in idxlist:
            tb = tburls[i]
            if tb:
                try:
                    r = cbtool.sendTrackback(tb,self.title,entry_url,
                                    blog_title,self.Description())
                    rls.append(r)
                    if len(r) >= 2 and r[0] == 0:
                        # Trackback has been added successfully
                        successfully_sent.append(tb)
                except:
                    pass
        [ tburls.remove(x) for x in successfully_sent ]
        self.setTrackback_url('\n'.join(tburls))
        self.setSent_trackback_url('\n'.join(successfully_sent))
        return rls

registerType(COREBlogEntry, PROJECTNAME)
