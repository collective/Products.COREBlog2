## Controller Python Script "validateComment"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
##

REQUEST=context.REQUEST

reqs = ['title','body']

#See setting and append required field list
if context.getComment_require_author():
    reqs.append('author')

if context.getComment_require_email():
    reqs.append('email')

if context.getComment_require_url():
    reqs.append('url')

errors = []

for key in reqs:
    if REQUEST.has_key(key) and not REQUEST[key]:
        state.setError(key, 'Please enter a value', new_status='failure')
        errors.append(key)

if state.getErrors():
    state.set(portal_status_message='Please correct the errors shown.')

return state

