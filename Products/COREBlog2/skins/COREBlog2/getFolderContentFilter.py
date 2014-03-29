## Python Script "getContentFilter"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Return ContentFilter,except for entry,CategoryFolder,CommentFolder
##

# Initialize filter dictionary
filter = {}

# Types to hide in contents tab
remove_types = ['COREBlogEntry',\
                'COREBlogCommentFolder','COREBlogCategoryFolder']

# Get types to allow to add in COREBlogFolder
types = [ tp.id for tp in context.getAllowedTypes()]

# Some folder automatically added, so add 'Folder' to types list
types.append('Folder')

# Loop over types to hide
for tp in remove_types:
    if tp in types:
        types.remove(tp)

filter['portal_type'] = types

# Return filter
return filter