## Controller Python Script "addComment"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Add comment to parent entry
##

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log

cbtool = getToolByName(context, 'coreblog2_tool')

REQUEST = context.REQUEST
form = REQUEST.form
RESPONSE = context.REQUEST.RESPONSE
entry = context

if REQUEST.form.has_key('remember_cookie'):
    #Set cookie
    for key in ['author','email','url']:
        if REQUEST.form.has_key(key):
            REQUEST.RESPONSE.setCookie(key,REQUEST.form[key],
                        path='/'.join(context.blog_object().getPhysicalPath()),
                        expires='Sun, 01-Dec-2099 12:00:00 GMT')

#Try to add comment
entry.addComment2Entry(author=form['author'],email=form['email'],
                        url=form['url'],title=form['title'],
                        body=form['body'],REQUEST=REQUEST)

#Send notify mail if need
if context.getSend_comment_notification():
    try:
        to_addr   = context.getNotify_to()
        from_addr = context.getNotify_to()
        msgbody = context.translate(msgid='comment_notify_body')
        elements = {}
        for k in ('title','author','url','body'):
            if REQUEST.form.has_key(k):
                elements[k] = REQUEST.form[k]
            else:
                elements[k] = ''
        elements['post_ip'] = REQUEST.getClientAddr()
        elements['entry_url'] = context.absolute_url()
        msgbody = msgbody % (elements)
        msgsubject = context.translate('comment_notify_title')
        mgsheader = """To: %s
From: %s
Mime-Version: 1.0
Content-Type: text/plain; Charset=utf-8

""" % (to_addr,from_addr)
        msgall = mgsheader+msgbody
        cbtool.send_mail(msgall, to_addr, from_addr, msgsubject)
    except Exception,e:
        log( 'COREBlog2/cbaddComment: '
                 'Some exception occured, %s' % e )

#Set next action
state.setNextAction('redirect_to:string:')

#Display message for user
state.setKwargs({'portal_status_message':'A comment successfully added.'})
return state



return state

