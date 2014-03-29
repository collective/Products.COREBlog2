##############################################################################
#
# contents/alias_proxy.py
#
# Copyright (c) 2007 Atsushi Shibata(shibata@webcore.co.jp).
#                                       All Rights Reserved.
#$Id: actions_proxy.py 229 2007-04-01 16:09:12Z ats $
#
# module for alias support for Plone 3.0 compatibility
#
##############################################################################

from Products.CMFCore.permissions import View, ModifyPortalContent

is_plone3 = True
try:
    from Products.ATContentTypes.content.base import updateActions
    is_plone3 = False
except:
    pass


from copy import copy
from inspect import isclass

def updateActions(klass_or_actions, actions):
    """Merge the actions from a class with a list of actions
    """
    if isclass(klass_or_actions):
        kactions = copy(klass_or_actions.actions)
    else:
        kactions = copy(klass_or_actions)

    aids  = [action.get('id') for action in actions ]
    actions = list(actions)

    for kaction in kactions:
        kaid = kaction.get('id')
        if kaid not in aids:
            actions.append(kaction)

    return tuple(actions)

def updateAliases(klass_or_aliases, aliases):
    """Merge the method aliases from a class with a dict of aliases
    """
    if isclass(klass_or_aliases):
        oldAliases = copy(klass_or_aliases.aliases)
    else:
        oldAliases = copy(klass_or_aliases)
    
    for aliasId, aliasTarget in oldAliases.items():
        if aliasId not in aliases:
            aliases[aliasId] = aliasTarget

    return aliases

base_actions = [{
        'id'          : 'view',
        'name'        : 'View',
        'action'      : 'string:${object_url}',
        'permissions' : (View,)
         },
        {
        'id'          : 'edit',
        'name'        : 'Edit',
        'action'      : 'string:${object_url}/edit',
        'permissions' : (ModifyPortalContent,),
         },
        {
        'id'          : 'metadata',
        'name'        : 'Properties',
        'action'      : 'string:${object_url}/properties',
        'permissions' : (ModifyPortalContent,),
         },
        ]


base_aliases = {
        '(Default)'  : '(dynamic view)',
        'view'       : '(selected layout)',
        'index.html' : '(dynamic view)',
        'edit'       : 'atct_edit',
        'properties' : 'base_metadata',
        'sharing'    : 'folder_localrole_form',
        'gethtml'    : '',
        'mkdir'      : '',
        }

if is_plone3:
    del base_actions[2]
    del base_aliases['properties']

