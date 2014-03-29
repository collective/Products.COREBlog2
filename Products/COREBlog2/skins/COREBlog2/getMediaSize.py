## Return referenced media content presentation
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=entry = None
##title=Return media size, setting for entry,'no_resize',(0,0) means no resize
##

if not entry:
    entry = container

# Sizes from ATContentType.content.image
sizes= {'large'   : (768, 768),
       'preview' : (400, 400),
       'mini'    : (200, 200),
       'thumb'   : (128, 128),
       'tile'    :  (64, 64),
       'icon'    :  (32, 32),
       'listing' :  (16, 16),
      }

sizestr = entry.getMedia_size()
if sizestr == 'no_resize' or not sizes.has_key(sizestr):
    return sizestr,0,0
else:
    return [sizestr] + list(sizes[sizestr])


