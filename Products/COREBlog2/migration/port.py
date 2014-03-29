## Controller Python Script "resetCookie"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Reset cookie for comment
##

import string
import DateTime

#parsing modes...
singleline_mode = 0
multiline_mode = 1
subcontent_mode = 2

#separetors
ml_sep = '-'*5
ent_sep = '-'*8
subcontents = ['comment','ping']

def parse_block(lines):
    #parsing a entry and store parts on dictionary
    d = {}
    mode = singleline_mode
    for line in lines:
        if mode == singleline_mode:
            pos = line.find(':')
            if pos != -1:
                #indicator was found.
                n = line[:pos].lower()
                v = line[pos+1:]
                d[n] = v.strip()
            elif line == ml_sep:
                #some multiline part start.
                mode = multiline_mode
                mn = ''
                continue
        elif mode == multiline_mode:
            if not mn:
                #First,
                pos = line.find(':')
                if pos != -1:
                    #set name of multiline part
                    mn = line[:pos].lower()
                else:
                    mode == singleline_mode
                if mn in subcontents:
                    mode = subcontent_mode
                    if not d.has_key(mn):
                        d[mn] = []
                        sn = mn
                    sd = {'body':''}
                    continue
                d[mn] = ''
                continue
            elif line == ml_sep:
                #start position of next multiline part
                mn = ''
            else:
                d[mn] = d[mn] + line + chr(0x0a)
        elif mode == subcontent_mode:
            pos = line.find(':')
            if pos != -1:
                #indicator was found.
                n = line[:pos].lower()
                v = line[pos+1:]
                sd[n] = v.strip()
            elif line == ml_sep:
                #some multiline part start.
                mode = multiline_mode
                mn = ''
                d[sn].append(sd)
                continue
            else:
                sd['body'] = sd['body'] + line + chr(0x0a)
    return d

def map_category(catname,catd,cbobj):
    if not catd.has_key(catname):
        #make new category
        cid = cbobj.getCategoryFolder().invokeFactory(id=catname, type_name='COREBlogCategory')
        a_id = 0
        for cat in cbobj.getCategoryFolder().objectValues(['COREBlogCategory']):
            try:
                a_id = max(cat.getInternal_id(),a_id)
            except:
                pass
        catobj = cbobj.getCategoryFolder()[cid]
        catobj.setInternal_id(a_id + 1)
        catobj.setTitle(catname)
        catobj.indexObject()
        catid = catobj.getInternal_id()
        catd[catname] = catid
    else:
        catid = catd[catname]
    return catid,catd

#retrive mt export file
mtobj = container['COREBlog_Export']

#retrive COREBlog instance
cbobj = context

#parse MT export  and find entry area
e = []

#ID - name dictiionary for category
catd = {}

for cat in cbobj.getCategoryFolder().objectValues():
    catd[cat.id] = cat.getInternal_id()

print "start!"

for line in str(mtobj.data).split(chr(0x0a)):
    if line == ent_sep:
        #A etnry block parsed!
        d = parse_block(e)
        #Initialize entry block list
        e = []
        #First, add category
        categoryids = []
        if d.has_key('primary category'):
            cid1,catd = map_category(d['primary category'],catd,cbobj)
            categoryids.append(str(cid1))
        if d.has_key('category'):
            cid2,catd = map_category(d['category'],catd,cbobj)
            subcat = [cid2]
            categoryids.append(str(cid2))
        else:
            subcat = []
        #Add entry
        md = 1
        if d['status'].lower() != 'publish':
            md = 0
        for k in ['extended body','excerpt']:
            if d.has_key(k) and d[k] == chr(0x0a):
                d[k] =''
        eid = cbobj.invokeFactory(id=d['id'], type_name='COREBlogEntry')
        ent = cbobj[eid]
        ent.setTitle(d['title'])
        ent.setBody(d['body'])
        ent.setExtend(d['extended body'])
        ent.setContentType('text/html','body')
        ent.setContentType('text/html','extended')
        ent.setDescription(d['excerpt'])
        ent.setEffectiveDate(d['date'])
        ent.setAllow_comment(str(int(d['allow comments'])+1))
        ent.setReceive_trackback(str(int(d['allow pings'])+1))
        ent.setEntry_categories('\n'.join(categoryids))
        ent.indexObject()
        print "-" * 40
        print d['id'],categoryids
        #add comments
        if d.has_key('comment') and len(d['comment']) > 0:
            for com in d['comment']:
                newid = ent.addComment2Entry(title="Re: " + d['title'],author=com['author'],
                                body=com['body'],email=com['email'],
                                    url=com['url'])
                comobj = cbobj.getCommentFolder()[newid]
                comobj.setEffectiveDate(com['date'])

        #add trackback
        if d.has_key('ping') and len(d['ping']) > 0:
            for tb in d['ping']:
                newid = ent.addTrackback2Entry(title=tb['title'],
                                excerpt=tb['body'],url=tb['url'],
                                blog_name=tb['blog name'])
                comobj = cbobj.getCommentFolder()[newid]
                comobj.setEffectiveDate(tb['date'])
    else:
        e.append(line)

print catd

return printed
