## Controller Python Script "resetCookie"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Receive trackback
##

# returns "one" enclosed object:

type_priorities = {'ATAudio':1,
                   'ATVideo':2,
                   'File':3,
                  }

eobj = None
pri = 10000

for obj in context.getRefs('relatesTo'):
    t = obj.portal_type
    if t in type_priorities.keys() and type_priorities[t] < pri:
        eobj = obj
        pri = type_priorities[t]

return eobj

