## Return referenced media content presentation
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj
##title=Return referenced media object's presentation
##

from Products.CMFCore.utils import getToolByName

INTERFACE = 'Products.COREBlog2.interfaces.IInlineObject.IInlineObject'

itool = getToolByName(context, 'portal_interface')

try:
    if itool.objectImplements(obj, INTERFACE) and obj.isInlineObject():
        tp,macro = obj.getInlineView()
        if tp and macro:
#            return container[tp].macros[macro]
            return getattr(context, tp).macros[macro]
except:
    pass

# Metal tempate for media handler
#tp = container['media_view']
tp = context.media_view
macro_keys = tp.macros.keys()
ct = ''
try:
    ct = '_' + obj.getContentType()
    ct = ct.replace('/','_')
except:
    pass

# First,see object portal_type and return appropreate template
otp = str(obj.portal_type).replace(' ','_')
lotp = obj.portal_type.lower()

key_trials = [otp,lotp,otp + ct,lotp + ct]

for trial in key_trials:
    if trial in macro_keys:
        # The macro for object is there !
        return tp.macros[trial]

# No custom template, so return object itself...
return tp.macros['Othrers__']


