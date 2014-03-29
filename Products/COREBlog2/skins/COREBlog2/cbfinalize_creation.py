## Controller Python Script "resetCookie"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=cbobj, ids
##title=Show archive
##

comment_folder_id, catetory_folder_id, stuff_folder_id, images_folder_id = ids

# create subfolders
if not hasattr(cbobj.aq_inner.aq_explicit, comment_folder_id):
    # Folder for comments/trackbacks
    cbobj.portal_types.constructContent('COREBlogCommentFolder',
                                       cbobj,
                                       comment_folder_id,
                                       title='Comments')

if not hasattr(cbobj.aq_inner.aq_explicit, catetory_folder_id):
    # Folder for categories
    cbobj.portal_types.constructContent('COREBlogCategoryFolder',
                                       cbobj,
                                       catetory_folder_id,
                                       title='Categories')
    ## Make default category
    #cat_folder = cbobj[catetory_folder_id]
    #cat_folder.constructContent('COREBlogCategory',
    #                            cbobj,
    #                            default_category_id,
    #                            title='Default')

if not hasattr(cbobj.aq_inner.aq_explicit, stuff_folder_id):
    # Folder for some stuff
    cbobj.portal_types.constructContent('Folder',
                                       cbobj,
                                       stuff_folder_id,
                                       title='Stuff')

if not hasattr(cbobj.aq_inner.aq_explicit, images_folder_id):
    # Folder for images
    cbobj.portal_types.constructContent('Folder',
                                       cbobj,
                                       images_folder_id,
                                       title='Images')
