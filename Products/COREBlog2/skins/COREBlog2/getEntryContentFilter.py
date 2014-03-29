## Python Script "getEntryContentFilter"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Return ContentFilter for entry listing
##
REQ = context.REQUEST

# Initialize filter dictionary
filter = {'portal_type':['COREBlogEntry'],
          'sort_on':'Date',
          'sort_order':'reverse'}

if REQ.form.has_key('SearchableText') and REQ.form['SearchableText']:
    filter['SearchableText'] = context.REQUEST.form['SearchableText']

if REQ.form.has_key('maxDate') and REQ.form.has_key('minDate') and \
    REQ.form['maxDate'] and REQ.form['minDate']:
    try:
        filter['Date'] = (DateTime(REQ.form['maxDate']),
                          DateTime(REQ.form['minDate']))
        filter['Date_usage'] = "range:max min"
    except:
        pass
elif REQ.form.has_key('maxDate') and REQ.form['maxDate']:
    filter['Date'] = (DateTime(REQ.form['maxDate']),DateTime('1999-01-01'))
    filter['Date_usage'] = "range:max min"
elif REQ.form.has_key('minDate') and REQ.form['minDate']:
    filter['Date'] = (DateTime('2999-12-31'),DateTime(REQ.form['minDate']))
    filter['Date_usage'] = "range:max min"

# Return filter
return filter