##############################################################################
#
# coreblog2.py
# Class for COREBlog2 Folder
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
#$Id: coreblog2.py 334 2007-09-06 03:37:37Z ats $
#$URL$
#$Rev: 334 $
#$Date: 2007-09-06 12:37:37 +0900 (Thu, 06 Sep 2007) $
#
##############################################################################

#Base classes
from Products.ATContentTypes.content.base import ATCTBTreeFolder
from Products.ATContentTypes.content.folder import ATBTreeFolder,\
                                                   ATBTreeFolderSchema,\
                                                   finalizeATCTSchema
from Products.ATContentTypes.interfaces import IATBTreeFolder
from Products.Archetypes.public import Schema,registerType
#Fields
from Products.Archetypes.public import StringField,IntegerField,TextField, \
                                   LinesField,ReferenceField,BooleanField
#Widgets
from Products.Archetypes.public import StringWidget,TextAreaWidget,\
                               IntegerWidget,SelectionWidget,BooleanWidget

from Products.Archetypes.utils import IntDisplayList
from Products.Archetypes.Marshall import PrimaryFieldMarshaller
from plone.app.upgrade.utils import safeEditProperty

from Products.COREBlog2.config import PROJECTNAME,\
                   comment_folder_id,catetory_folder_id,\
                   stuff_folder_id,images_folder_id,default_category_id,\
                   coreblog2_meta_type,coreblogentry_meta_type,\
                   coreblogcomment_meta_type,coreblogtrackback_meta_type,\
                   coreblogcategory_meta_type,far_far_past,far_far_future
from Products.COREBlog2.content.coreblogentry\
                 import COREBlogEntry,comment_status,trackback_status

from Products.COREBlog2.configuration import zconf

from actions_proxy import updateAliases, updateActions, \
                          base_actions, base_aliases

from DateTime import DateTime

from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import View,ListFolderContents,\
                    ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from zope.interface import implements

import calendar
import os.path
import sys
from copy import deepcopy

from zope.component import getUtility, getMultiAdapter
from zope.app.container.interfaces import INameChooser

#new style portlet
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.app.portlets.interfaces import IPortletPermissionChecker
from plone.app.portlets.portlets import classic
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.constants import CONTEXT_CATEGORY

__doc__="""Blog Product for Plone 'COREBlog:COREBlog'
$Id: coreblog2.py 334 2007-09-06 03:37:37Z ats $"""

COREBLOG2_DIR = os.path.abspath(os.path.dirname(__file__))
COREBLOG2_DIR = os.path.join(COREBLOG2_DIR,os.path.pardir)

__version__ = open(os.path.join(COREBLOG2_DIR,'version.txt')).read().strip()
__product_version__ = "COREBlog2 " + __version__

__author__  = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'

COREBlog2Schema = ATBTreeFolder.schema.copy() +  Schema((

    #Basic settings
    TextField('long_description',
        searchable=1,
        default='',
        allowable_content_types = ('text/plain', ),
        widget=TextAreaWidget(label='Long description',
                    description='',
                    label_msgid='label_long_description',
                    description_msgid='help_long_description',
                    i18n_domain='plone',
                    cols=60,rows=5),
        ),

    #Entry listing
    IntegerField('top_entry_count_setting',
        searchable=0,
        default=1,
        widget=SelectionWidget(label='Entries per page',
                    description='',
                    label_msgid='label_top_entry_count_setting',
                    description_msgid='help_top_entry_count_setting',
                    i18n_domain='plone',
                    ),
        vocabulary=IntDisplayList((
                    (1, 'In days', 'label_show_entry_in_days'),
                    (2, 'In entry count', 'label_show_entry_in_count'),
                    )),
        schemata='cbsettings_display',
        ),

    IntegerField('top_entry_count',
        searchable=0,
        default = zconf.coreblog2.top_entry_count_default,
        widget=IntegerWidget(label='Entries count',
                    description='',
                    label_msgid='label_top_entry_count',
                    description_msgid='help_top_entry_count',
                    i18n_domain='plone',
                    ),
        schemata='cbsettings_display',
        ),

    IntegerField('portlet_item_count',
        searchable=0,
        default = zconf.coreblog2.portlet_item_count_default,
        widget=IntegerWidget(label='Items per portlet',
                    description='',
                    label_msgid='label_portlet_item_count',
                    description_msgid='help_portlet_item_count',
                    i18n_domain='plone',
                    ),
        schemata='cbsettings_display',
        ),

    IntegerField('batch_size',
        searchable=0,
        default = zconf.coreblog2.batch_size_default,
        widget=IntegerWidget(label='Batch size',
                    description='',
                    label_msgid='label_batch_size',
                    description_msgid='help_batch_size',
                    i18n_domain='plone',
                    ),
        schemata='cbsettings_display',
        ),

    #Entry
    StringField('entrydate_format',
        searchable=0,
        default = '%Y/%m/%d',
        widget=StringWidget(label='Entrydate format',
                    description='',
                    label_msgid='label_entrydate_format',
                    description_msgid='help_entrydate_format',
                    i18n_domain='plone',
                    size=60,
                    ),
        schemata='cbsettings_display',
        ),

    #PING/Trackback
    StringField('trackback_base',
        searchable=0,
        default='',
        widget=StringWidget(label='Trackback base URL',
                    description='',
                    label_msgid='label_trackback_base',
                    description_msgid='help_trackback_base',
                    i18n_domain='plone',
                    size=60,
                    ),
        schemata='cbsettings_entry',
        ),

    TextField('ping_servers',
        searchable=1,
        default='',
        allowable_content_types = ('text/plain', ),
        widget=TextAreaWidget(label='Ping servers',
                    description='',
                    label_msgid='label_ping_servers',
                    description_msgid='help_ping_servers',
                    i18n_domain='plone',
                    cols=60,rows=5,
                    ),
        schemata='cbsettings_entry',
        ),


    StringField('body_default_format',
        searchable=0,
        default = 'text/html',
        widget=SelectionWidget(label='Default format for entry body',
                    description='',
                    label_msgid='label_body_default_format',
                    description_msgid='help_body_default_format',
                    i18n_domain='plone',
                    ),
        vocabulary=zconf.coreblog2.allowed_content_types ,
        schemata='cbsettings_entry',
        ),

    IntegerField('allow_comment_default',
        searchable=0,
        default = COREBlogEntry.comment_open,
        widget=SelectionWidget(label='Default comment status',
            label_msgid='label_allow_comment_default',
            i18n_domain='plone',),
        vocabulary=IntDisplayList(comment_status),
        schemata='cbsettings_entry',
        ),

    IntegerField('receive_trackback_default',
        searchable=0,
        default = COREBlogEntry.trackback_open,
        widget=SelectionWidget(label='Default trackback status',
            label_msgid='label_receive_trackback_default',
            i18n_domain='plone',),
        vocabulary=IntDisplayList(trackback_status),
        schemata='cbsettings_entry',
        ),

    BooleanField('dont_send_ping',
        searchable=1,
        default=zconf.coreblog2.dont_send_ping_default,
        widget=BooleanWidget(\
                    label='Don\'t send PING/Trackback when entry added.',
                    description='',
                    label_msgid='label_dont_send_ping',
                    description_msgid='help_dont_send_ping',
                    i18n_domain='plone',
                    ),
        schemata='cbsettings_entry',
        ),

    #Comment validation
    BooleanField('comment_require_author',
        searchable=1,
        default=True,
        widget=BooleanWidget(label='Require author',
                    description='',
                    label_msgid='label_comment_require_author',
                    description_msgid='help_comment_require_author',
                    i18n_domain='plone',
                    ),
        schemata='cbsettings_comment_trackback',
        ),

    BooleanField('comment_require_email',
        searchable=1,
        default=True,
        widget=BooleanWidget(label='Require email',
                    description='',
                    label_msgid='label_comment_require_email',
                    description_msgid='help_comment_require_email',
                    i18n_domain='plone',
                    ),
        schemata='cbsettings_comment_trackback',
        ),

    BooleanField('comment_require_url',
        searchable=1,
        default=True,
        widget=BooleanWidget(label='Require URL',
                    description='',
                    label_msgid='label_comment_require_url',
                    description_msgid='help_comment_require_url',
                    i18n_domain='plone',
                    ),
        schemata='cbsettings_comment_trackback',
        ),

    #Nortifications
    BooleanField('send_comment_notification',
        searchable=1,
        default=True,
        widget=BooleanWidget(label='Send a notification mail on new comment',
                    description='',
                    label_msgid='label_send_comment_notification',
                    description_msgid='help_send_comment_notification',
                    i18n_domain='plone',
                    ),
        schemata='cbsettings_comment_trackback',
        ),

    BooleanField('send_trackback_notification',
        searchable=1,
        default=True,
        widget=BooleanWidget(label='Send a notification mail on new trackback',
                    description='',
                    label_msgid='label_send_trackback_notification',
                    description_msgid='help_send_trackback_notification',
                    i18n_domain='plone',
                    ),
        schemata='cbsettings_comment_trackback',
        ),

    StringField('notify_from',
        searchable=1,
        widget=StringWidget(label='Notify From',
                    description='',
                    label_msgid='label_notify_from',
                    description_msgid='help_notify_from',
                    i18n_domain='plone',
                    size=60),
        schemata='cbsettings_comment_trackback',
        ),

    StringField('notify_to',
        searchable=1,
        widget=StringWidget(label='Notify To',
                    description='',
                    label_msgid='label_notify_to',
                    description_msgid='help_notify_to',
                    i18n_domain='plone',
                    cols=60,rows=2, size=80),
        schemata='cbsettings_comment_trackback',
        ),


    ),
    )

#Finalize schema definition
finalizeATCTSchema(COREBlog2Schema)

class COREBlog2(ATBTreeFolder):
    """
    This is a COREBlog2 class,
    base folder for COREBlog2
    """
    
    archetype_name = "COREBlog2"
    meta_type = coreblog2_meta_type
    suppl_views    = ()

    schema = COREBlog2Schema

    _at_rename_after_creation = True

    implements(IATBTreeFolder)

    security = ClassSecurityInfo()

    actions = updateActions(deepcopy(base_actions),(
        {
        'id': 'entrylisting',
        'name': 'Entries',
        'action': 'string:${object_url}/entry_listing',
        'permissions': (ListFolderContents,),
            },
        {
        'id': 'category',
        'name': 'Categories',
        'action': 'string:${object_url}/categories',
        'permissions': (ListFolderContents,)
            },
            ))

    aliasdict = {
                'folder_contents' : 'cbfolder_contents',
                'view' : 'coreblog_view',
                'edit' : 'blogsettings_edit',
                }

    aliases = updateAliases(deepcopy(base_aliases), aliasdict)

    def initializeArchetype(self, **kwargs):
        ATBTreeFolder.initializeArchetype(self, **kwargs)

        left = getUtility(IPortletManager, name='plone.leftcolumn')
        right = getUtility(IPortletManager, name='plone.rightcolumn')
        
        leftAssignable = getMultiAdapter((self, left), IPortletAssignmentMapping).__of__(self)
        rightAssignable = getMultiAdapter((self, right), IPortletAssignmentMapping).__of__(self)
        
#        IPortletPermissionChecker(leftAssignable)()
#        IPortletPermissionChecker(rightAssignable)()
        
        leftChooser = INameChooser(leftAssignable)
        rightChooser = INameChooser(rightAssignable)
        

        # Set slot properties
        left_slots = zconf.coreblog2.left_slots_default
        for item in left_slots:
            path = item.split('/')
            if len(path) == 4:
                newPortlet = classic.Assignment(path[1], path[3])
                leftAssignable[leftChooser.chooseName(None, newPortlet)] = newPortlet

        right_slots = zconf.coreblog2.right_slots_default
        for item in right_slots:
            path = item.split('/')
            if len(path) == 4:
                newPortlet = classic.Assignment(path[1], path[3])
                rightAssignable[rightChooser.chooseName(None, newPortlet)] = newPortlet
        
        labLeftColumnManager = getMultiAdapter((self, left), ILocalPortletAssignmentManager)
        labLeftColumnManager.setBlacklistStatus(CONTEXT_CATEGORY, True)
        labRightColumnManager = getMultiAdapter((self, right), ILocalPortletAssignmentManager)
        labRightColumnManager.setBlacklistStatus(CONTEXT_CATEGORY, True) 
        
        # finalize
        # make subfolders, etc.
        self.cbfinalize_creation(self,
                                (comment_folder_id, catetory_folder_id, 
                                 stuff_folder_id, images_folder_id))
        self.indexObject()

    def canSetDefaultPage(self):
        return True

    security.declarePrivate('setLong_description')
    def setLong_description(self, value, **kwargs):
        #
        # The setter for long_description, also making copy to 'description',
        #
        self.getField('long_description').set(self, value, **kwargs)
        transformer = getToolByName(self,'portal_transforms')
        flat_desc =  transformer.convertToData('text/plain',\
                                        self.getLong_description())
        orig_len = len(flat_desc)
        flat_desc = flat_desc.replace('\n','')
        flat_desc = flat_desc.replace('\r','')
        self.setDescription(flat_desc)

    security.declareProtected(View,'blog_url')
    def blog_url(self):
        return self.absolute_url()

    security.declareProtected(View,'blog_object')
    def blog_object(self):
        return self

    #
    # Catalog queries for object listing
    #

    security.declareProtected(View,'getRecentEntry')
    def getRecentEntry(self,type=0,limit=0,\
                       sort_on='Date',sort_order='reverse',\
                       full_objects=True):
        #
        # Returns recent entries
        # for entry list on blog's top page
        #

        # Make dictionary for query arguments
        path = {}
        path['query'] = '/'.join(self.getPhysicalPath())
        path['depth'] = 1
        args = {}
        args['path'] = path
        if not type:
            type = self.getTop_entry_count_setting()
        if not limit:
            limit = self.getTop_entry_count()

        args['meta_type'] = [coreblogentry_meta_type]
        args['sort_on'] = sort_on
        args['sort_order'] = sort_order

        if type == 1:
            # If type is 1,show entries for dates.
            # So we need to find date of most recent entry.
            args['sort_limit'] = 1
            args["Date"] = {'query' : [DateTime(far_far_past), DateTime()],
                            'range' : 'minmax'}
            recent_entries = self.portal_catalog(show_inactive=False,**args)
            if recent_entries:
                recent_date = recent_entries[0].Date
            else:
                recent_date = DateTime()
            args["Date"] = {'query' : [DateTime(recent_date)-limit-1, DateTime(recent_date)],
                            'range' : 'minmax'}
            del args['sort_limit']
        else:
            args["Date"] = {'query' : [DateTime(far_far_past), DateTime()],
                            'range' : 'minmax'}
            args['sort_limit'] = limit

        # Initialize list to return
        objs = self.portal_catalog(show_inactive=False,**args)
       
        if full_objects:
            objs = [b.getObject() for b in objs]

        return objs

    security.declareProtected(View,'getRecentEntry')
    def synContentValues(self):
        #
        # play nice with portal_syndication_tool
        #
        return self.getRecentEntry()


    security.declareProtected(View,'getEntryInDate')
    def getEntryInDate(self,year,month,day=0,\
                       batch=False,b_size=0,b_start=0,\
                       sort_on='Date',sort_order='',\
                       full_objects=True):
        #
        # Return entryes in specific month,or day
        # Used for calender portlet and 
        #

        # Make dictionary for query arguments
        path = {}
        path['query'] = '/'.join(self.getPhysicalPath())
        path['depth'] = 1
        s_args = {}
        s_args['meta_type'] = [coreblogentry_meta_type]
        s_args['path'] = path
        if day:
            startday = day
            endday = day
        else:
            #Find month daycount
            startday = 1
            endday = calendar.monthrange(year,month)[1]
        start_date = DateTime("%d-%d-%d 00:00:00" % (year,month,startday))
        end_date = DateTime("%d-%d-%d 23:59:59" % (year,month,endday))
        if DateTime() < end_date:
            # Hide future entries
            end_date = DateTime()
        s_args['Date'] = { "query": [start_date, end_date],
                         "range": "minmax" }
        s_args['sort_on'] = sort_on
        s_args['sort_order'] = sort_order
        # Initialize list to return
        objs = self.portal_catalog(show_inactive=False, **s_args)

        if full_objects:
            objs = [b.getObject() for b in objs]

        if batch:
            from Products.CMFPlone import Batch
            batch = Batch(objs, b_size, int(b_start), orphan=0)
            return batch

        return objs

    security.declareProtected(View,'getEntryForCalendar')
    def getEntryForCalendar(self, month, year):
        #
        # Returns entries on month,
        # For every days in calendar,if entry exists,
        # store data for mapping following...
        # {'day': #, 'entry': None}
        #
        year=int(year)
        month=int(month)

        daysByWeek=calendar.monthcalendar(year, month)
        weeks=[]

        enteirs_in_month=self.getEntryInDate(year,month,full_objects=False)
        entries = {}
        for entry in enteirs_in_month:
            day = DateTime(entry.Date).day()
            entries[day] = 1

        for week in daysByWeek:
            days=[]
            for day in week:
                if entries.has_key(day):
                    days.append({'day':day,'entry':1})
                else:
                    days.append({'day':day,'entry':None})

            weeks.append(days)

        return weeks

    security.declareProtected(View,'getNearestEntry')
    def getNearestEntry(self,base_date,sort_order='reverse',\
                        sort_on='Date',full_objects=True):
        #
        # Returns nearest entries
        #

        # Make dictionary for query arguments
        path = {}
        path['query'] = '/'.join(self.getPhysicalPath())
        path['depth'] = 1
        args = {}

        args['path'] = path
        args['meta_type'] = [coreblogentry_meta_type]
        args['sort_on'] = sort_on
        args['sort_order'] = sort_order

        args['sort_limit'] = 2
        if sort_order == 'reverse':
            args["Date"] = {'query' : [DateTime(far_far_past), DateTime(base_date)],
                            'range' : 'minmax'}
        else:
            args["Date"] = {'query' : [DateTime(base_date), DateTime(far_far_future)],
                            'range' : 'minmax'}

        # Initialize list to return
        objs = self.portal_catalog(show_inactive=False,**args)

        if full_objects:
            objs = [b.getObject() for b in objs]

        return objs

    security.declarePrivate('getRecentItem')
    def getRecentItem(self,limit=0,meta_types=[],\
                        sort_on='Date',sort_order='',full_objects=True):
        # Make dictionary for query arguments
        path = {}
        path['query'] = '/'.join(self.getCommentFolder().getPhysicalPath())
        path['depth'] = 1
        args = {}
        args['path'] = path
        args["Date"] = {'query' : [DateTime(far_far_past), DateTime()],
                        'range' : 'minmax'}
        if not limit:
            limit = self.getPortlet_item_count()

        args['meta_type'] = meta_types
        args['sort_on'] = sort_on
        args['sort_order'] = sort_order

        args['sort_limit'] = limit

        # Initialize list to return
        objs = self.portal_catalog(show_inactive=False,**args)

        if full_objects:
            objs = [b.getObject() for b in objs]

        return objs


    security.declareProtected(View,'getRecentComment')
    def getRecentComment(self,limit=0,\
                       sort_on='Date',sort_order='reverse',\
                       full_objects=True):
        #
        # Returns recent comments
        #
        return self.getRecentItem(meta_types=[coreblogcomment_meta_type],\
                                  sort_on=sort_on,sort_order=sort_order,\
                                  full_objects=full_objects)


    security.declareProtected(View,'getRecentTrackback')
    def getRecentTrackback(self,limit=0,\
                       sort_on='Date',sort_order='reverse',\
                       full_objects=True):
        #
        # Returns recent trackback
        #
        return self.getRecentItem(meta_types=[coreblogtrackback_meta_type],\
                                  sort_on=sort_on,sort_order=sort_order,\
                                  full_objects=full_objects)


    #
    # Accessor for subfolders
    #

    security.declareProtected(View,'getCategoryFolder')
    def getCategoryFolder(self):
        """
        Return Category Folder
        """
        return self[catetory_folder_id]

    security.declareProtected(View,'getCommentFolder')
    def getCommentFolder(self):
        """
        Return Comment Folder
        """
        return self[comment_folder_id]

    #
    # Category management
    #

    security.declareProtected(View,'getEntryInCategory')
    def getEntryInCategory(self,category_ids,\
                       sort_on='Date',sort_order='',\
                       batch=False,b_size=0,b_start=0,\
                       full_objects=True):
        #
        # Return entryes in specific category(s)
        #

        # Make dictionary for query arguments
        path = {}
        path['query'] = '/'.join(self.getPhysicalPath())
        path['depth'] = 1
        args = {}
        args['path'] = path
        args['meta_type'] = [coreblogentry_meta_type]
        category_ids_s = [str(category_ids[0])]
        args['getEntry_categories'] = category_ids_s

        args['meta_type'] = [coreblogentry_meta_type]
        args['sort_on'] = sort_on
        args['sort_order'] = sort_order

        # Initialize list to return
        objs = self.portal_catalog(show_inactive=False,**args)

        if len(category_ids) > 1:
            for chk_cat in category_ids[1:]:
                objs = [ o for o in objs
                        if str(chk_cat) in o.getObject().entry_categories ]

        if full_objects:
            objs = [b.getObject() for b in objs]

        if batch:
            from Products.CMFPlone import Batch
            batch = Batch(objs,b_size, int(b_start), orphan=0)
            return batch

        return objs

    security.declareProtected(View,'getCategoryCount')
    def getCategoryCount(self,category_title, sort_on='Date'):
        #
        # Return entrye countn in a given category
        #

        path = {}
        path['query'] = '/'.join(self.getPhysicalPath())
        path['depth'] = 1
        args = {}
        #args['path'] = path
        args['meta_type'] = [coreblogentry_meta_type]
        args['getTags'] = category_title
#        try:
#            args['getTags'] = unicode(category_title, 'utf-8', 'ignore')
#        except:
#            pass

        args['meta_type'] = [coreblogentry_meta_type]
        args['sort_on'] = sort_on

        # Initialize list to return
        objs = self.portal_catalog(show_inactive=False,**args)

        return len(objs)


    security.declareProtected(View, 'getCategoryMap')
    def getCategoryMap(self,full_objects=True):
        #Returns category mapping
        cat_d = {}
        catfolder = self.getCategoryFolder()
        if full_objects:
            # Infrate real object
            for cat_obj in catfolder.objectValues(coreblogcategory_meta_type):
                cat_d[str(cat_obj.getInternal_id())] = \
                        {'title':cat_obj.title,'id':cat_obj.id,
                         'url':cat_obj.absolute_url(),
                         'obj':cat_obj }
        else:
            path = {}
            path['query'] = '/'.join(catfolder.getPhysicalPath())
            path['depth'] = 1
            contentFilter = {'path':path,\
                             'portal_type':coreblogcategory_meta_type}
            for cat_obj in \
                self.portal_catalog.queryCatalog(contentFilter,show_all=1):
                cat_d[str(cat_obj.getInternal_id)] = \
                        {'title':cat_obj.title,'id':cat_obj.id,
                         'url':catfolder.absolute_url() + '/' + cat_obj.id}
        return cat_d


    security.declareProtected(View, 'getCategoryById')
    def getCategoryById(self,id,full_objects=True):
        #Returns category by internal ID
        cat_folder = self[catetory_folder_id]
        path = {}
        path['query'] = '/'.join(cat_folder.getPhysicalPath())
        path['depth'] = 1
        contentFilter = {'path':path,'portal_type':coreblogcategory_meta_type}
        for cat_obj in \
            self.portal_catalog.queryCatalog(contentFilter,show_all=1):
            if str(cat_obj.getInternal_id) == str(id):
                if full_objects:
                    return cat_obj.getObject()
                else:
                    return cat_obj
        return None

    #
    # Sending PING
    #
    security.declareProtected(ModifyPortalContent, 'sendPing')
    def sendPing(self,idx = -1):
        """
        Send ping to servers on setting.
        If any idx served, only one ping will be sent.
        If idx == -1, try to send all ping servers.
        """
        cbtool = getToolByName(self,'coreblog2_tool')
        blogurl = self.absolute_url()
        if self.getTrackback_base():
            blogurl = self.getTrackback_base()
        try:
            svs = self.getPing_servers().split('\n')
        except:
            svs = self.getPing_servers()
        indexlist = range(0,len(svs))
        if idx != -1:
            indexlist = [index]
        rl = []
        for i in indexlist:
            if svs[i].find('http:') == 0:
                r = cbtool.sendPing(svs[i],self.title,blogurl,
                                __product_version__)
                rl.append(r)
        return rl

    #
    # Misc methods
    #

    security.declareProtected(View, 'getEntryFieldOrder')
    def getEntryFieldOrder(self):
        #
        #Returns edit field order for entry
        #
        return ['id','title','subtitle','entry_categories','body','extend',
                'allow_comment','receive_trackback','relatedItems',
                'media_position','media_size']

registerType(COREBlog2,PROJECTNAME)

