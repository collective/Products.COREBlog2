#$Id: config.py 214 2007-01-06 13:11:15Z ats $

from Products.CMFCore.permissions import AddPortalContent
from Products.COREBlog2.configuration import zconf

ADD_CONTENT_PERMISSION = 'Add COREBlog2'
PROJECTNAME = "COREBlog2"
SKINS_DIR = 'skins'

GLOBALS = globals()

comment_folder_id = 'comments'
catetory_folder_id = 'categories'
stuff_folder_id = 'stuff'
images_folder_id = 'images'

default_category_id = 'default'

#Relationship id
comemnt_rel_id = 'entrycomments'
trackback_rel_id = 'entrytrackbacks'

#Meta types
coreblog2_meta_type = 'COREBlog2'
coreblogentry_meta_type = 'COREBlogEntry'
coreblogcomment_meta_type = 'COREBlogComment'
coreblogtrackback_meta_type = 'COREBlogTrackback'
coreblogcategory_meta_type = 'COREBlogCategory'

far_far_past = '1000/01/01'
far_far_future= '2999/01/01'