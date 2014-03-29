## Controller Python Script "resetCookie"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Receive trackback
##

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log

cbtool = getToolByName(context, 'coreblog2_tool')

REQUEST = context.REQUEST
form = REQUEST.form
RESPONSE = context.REQUEST.RESPONSE
entry = context

excerpt = ''
if form.has_key('excerpt'):
    excerpt = form['excerpt']

title = cbtool.convert_charcode(form['title'])
blog_name = cbtool.convert_charcode(form['blog_name'])
excerpt = cbtool.convert_charcode(excerpt)
url = cbtool.convert_charcode(form['url'])

#Try to add trackback
try:
    #Send notify mail if need
    if context.getSend_trackback_notification():
        try:
            to_addr   = context.getNotify_to()
            from_addr = context.getNotify_to()
            msgbody = context.translate('trackback_notify_body')
            elements = {}
            for k in ('blog_name','title','excerpt','url','excerpt'):
                if form.has_key(k):
                    elements[k] = REQUEST.form[k]
                else:
                    elements[k] = ''
            elements['post_ip'] = REQUEST.getClientAddr()
            elements['entry_url'] = context.absolute_url()
            msgbody = msgbody % (elements)
            msgsubject = context.translate('trackback_notify_title')
            mgsheader = """To: %s
From: %s
Mime-Version: 1.0
Content-Type: text/plain; Charset=utf-8

""" % (to_addr,from_addr)
            cbtool.send_mail(mgsheader+msgbody, to_addr, from_addr, msgsubject)
        except Exception,e:
            log( 'COREBlog2/tbping: '
                     'Some exception occured, %s' % e )

    entry.addTrackback2Entry(title=title,url=url,\
                            blog_name=blog_name,excerpt=excerpt)
    
    return context.tbping_result(client=context,REQUEST=REQUEST,\
                                        error_code=0,message='Thanks :-)')
except:
    return context.tbping_result(client=context,REQUEST=REQUEST,\
                                    error_code=1,message='Error occured!')

