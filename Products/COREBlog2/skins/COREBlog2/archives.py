## Controller Python Script "resetCookie"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Show archive
##

from DateTime import DateTime

REQUEST = context.REQUEST
form = REQUEST.form

# Set current year,moth

year = DateTime().year()
month = DateTime().month()
day = None

go_redirect = False

if len(traverse_subpath) <= 1:
    # Redirect when called without traverse_subpath,or 
    go_redirect = True
else:
    #Check if all subpath are integer
    try:
        year = int(traverse_subpath[0])
        month = int(traverse_subpath[1])
        if len(traverse_subpath) >= 3:
            day = int(traverse_subpath[2])
    except:
        go_redirect = True

    #Check for number validation
    if year <= 0:
        go_redirect = True
    if month <= 0 or month > 12:
        go_redirect = True

if go_redirect:
    REQUEST.RESPONSE.redirect('../')

return context.cbarchive_view(year=year,month=month,day=day)
