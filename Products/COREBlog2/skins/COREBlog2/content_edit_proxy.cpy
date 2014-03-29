## Script (Python) "content_edit_proxy"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=id=''
##

# Call original content_edit method,
# to store edited context to ZODB

rst = context.content_edit_impl(state, id)

new_context = context

try:
    new_context = rst.getContext()
except:
    pas

#Check for PING/Trackback settings
if not new_context.getDont_send_ping():
    # Try to send PING
    if state.getStatus() != 'next_schemata' and \
       not new_context.hasPingSent():
        ping_states = new_context.sendPing()
        new_context.setPingStatus(True)
    #Try to send trackbacks
    tb_state = new_context.sendTrackbacks()

# Return status
return rst

