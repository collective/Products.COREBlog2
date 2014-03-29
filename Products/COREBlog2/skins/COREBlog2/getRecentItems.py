## Return referenced media content presentation
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Return referenced attachment content presentation
##

from Products.CMFCore.utils import getToolByName

# Get plone_utils instance
putil = getToolByName(container,'plone_utils')

# Portal types to list

typesToShow = putil.getUserFriendlyTypes()

for tp in ['COREBlog2','COREBlogEntry','COREBlogCategory',
           'COREBlogComment','COREBlogTrackback',
           'COREBlogCategoryFolder','COREBlogCommentFolder',
           'Folder',]:
    if tp in typesToShow:
        typesToShow.remove(tp)

res = container.portal_catalog.searchResults(sort_on='modified',
                       path='/'.join(context.aq_parent.getPhysicalPath()),
                       portal_type=typesToShow,
                       sort_order='reverse')[:8]

return res
