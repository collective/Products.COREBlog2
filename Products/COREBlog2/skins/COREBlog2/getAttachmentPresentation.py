## Return referenced media content presentation
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj
##title=Return referenced attachment content presentation
##

# !!!
# Handling for Content-type, File:swf,mp3,mpeg4 or something
#

# Metal tempate for media handler
tp = container['cbattachment_view']
macro_keys = tp.macros.keys()

# First,see object portal_type and return appropreate template
if obj.portal_type in macro_keys:
    # The macro for object is there !
    return tp.macros[obj.portal_type]

if obj.portal_type.lower() in macro_keys:
    # The macro for object is there !
    return tp.macros[obj.portal_type.lower()]

# No custom template, so return object itself...
return tp.macros['Othrers__']



