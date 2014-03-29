## Return referenced object by kind
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=kind='media'
##title=Show archive
##

# !!!
# Handling for Content-type, File:swf,mp3,mpeg4 or something
#
from Products.CMFCore.utils import getToolByName

INTERFACE = 'Products.COREBlog2.interfaces.IInlineObject.IInlineObject'

itool = getToolByName(context, 'portal_interface')

# Portal types for media
media_types = ('Image', 'ATVideo', 'Amazon Item',
               'File:video/quicktime', 'File:video/x-ms-wmv')

ret_l = []

# Get referenced objects
for obj in context.getRefs('relatesTo'):
    try:
        ct = ''
        try:
            ct = ':' + obj.getContentType()
        except:
            pass
        if obj.portal_type in media_types or \
           obj.portal_type + ct in media_types or \
           itool.objectImplements(obj, INTERFACE):
            if kind == 'media':
                ret_l.append(obj)
        elif kind != 'media':
            ret_l.append(obj)
    except:
        pass

return ret_l