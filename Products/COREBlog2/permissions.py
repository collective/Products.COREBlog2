#permissions.py
#
#$Id: permissions.py 215 2007-01-06 15:06:34Z ats $

from Products.CMFCore.permissions import setDefaultRoles
import Products.Archetypes.public as atapi
import config

def initialize():
    permissions = {}
    types = atapi.listTypes(config.PROJECTNAME)
    for atype in  types:
        permission = "%s: Add %s" % (config.PROJECTNAME, atype['portal_type'])
        permissions[atype['portal_type']] = permission
        setDefaultRoles(permission, ('Manager','Owner'))

    return permissions

setDefaultRoles( 'COREBlog2: Add COREBlogComment',
                            ( 'Anonymous', 'Manager', 'Owner' ) )
setDefaultRoles( 'COREBlog2: Add COREBlogTrackback',
                            ( 'Anonymous', 'Manager', 'Owner' ) )

