## Controller Python Script "resetCookie"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Reset cookie for comment
##

RESPONSE = context.REQUEST.RESPONSE

for key in ['author','email','url']:
    RESPONSE.expireCookie(key)

#Set next action
state.setNextAction('redirect_to:string:entry_view')

state.setKwargs({})

return state

