##############################################################################
#
# COREBlogFolder.py
# Class for COREBlog2 Folder
#
# Copyright (c) 2005 Atsushi Shibata(shibata@webcore.co.jp).
#                                       All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its 
# documentation for any purpose and without fee is hereby granted, provided that
# the above copyright notice appear in all copies and that both that copyright 
# notice and this permission notice appear in supporting documentation, and that
# the name of Atsushi Shibata not be used in advertising or publicity pertaining 
# to distribution of the software without specific, written prior permission. 
# 
# ATSUSHI SHIBAT DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, 
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
# EVENT SHALL SHIBAT ATSUSHI BE LIABLE FOR ANY SPECIAL, INDIRECT OR 
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
# USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE. 
#
#$Id: COREBlogTool.py 213 2007-01-06 13:10:33Z ats $
#
##############################################################################

from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log

from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from Globals import InitializeClass

from Products.COREBlog2.configuration import zconf

#Python modules
import urllib
import string,urllib,httplib,urlparse,re
from xmlrpclib import Server,Transport
import socket

timeout = zconf.coreblog2.ping_timeout_default

def safe_uencode(s):
    if isinstance(s,unicode):
        s = s.encode('utf-8')
    else:
        s = unicode(s,'utf-8').encode('utf-8')
    return s

class COREBlog2Tool(UniqueObject, SimpleItem):
    """Utility methods for COREBlog2"""

    id = 'coreblog2_tool'
    meta_type= 'COREBlog2 Tool'
    plone_tool = True

    security = ClassSecurityInfo()

    security.declarePublic('sendPing')
    def sendPing(self,
                 serverurl,
                 blogtitle,
                 url,
                 version_str = "COREBlog2",
                 char_code = "utf-8",
                 fromcode=""):
        """
           Send PING to PING server.
        """
        #blogtitle = convert_charcode(blogtitle,char_code,fromcode)
        # Sotre timeout
        oldtimeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)

        svr = Server(serverurl)
        Transport.user_agent = version_str

        try:
            resp = svr.weblogUpdates.ping(blogtitle,url)
        except Exception, e:
            resp = {'error':str(e)}

        socket.setdefaulttimeout(oldtimeout)

        return resp

    security.declarePublic('sendTrackback')
    def sendTrackback(self,
                  trackback_url,
                  title="",
                  src_url="",
                  blog_name="",
                  excerpt="",
                  agent = "COREBlog2",
                  charset="utf-8",
                  param_charset="utf-8"):
        """
        Try to send trackback request to trackback_url
        """
        try:
            #To make dictionary for POST
            params = {"title":    safe_uencode(title),
                      "url":      safe_uencode(src_url),
                      "blog_name":safe_uencode(blog_name),
                      }
            headers = ({"Content-type": "application/x-www-form-urlencoded",
                        "User-Agent": agent})
    
            if param_charset:
                params["charset"] = param_charset
            elif charset:
                headers["Content-type"] = headers["Content-type"] + \
                                                    "; charset=%s"
            # Sotre timeout
            oldtimeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(timeout)
    
            if len(excerpt) > 0:
                params["excerpt"] = safe_uencode(excerpt)
    
            tb_url_t = urlparse.urlparse(trackback_url)
            enc_params = urllib.urlencode(params)
    
            #check if trackback url contains parameter section(for PyDs!)
            ut = urlparse.urlparse(trackback_url)
            if len(ut) >= 4 and ut[4]:
                #add params to parameter section
                enc_params = ut[4] + '&' + enc_params
    
            host = tb_url_t[1]
            path = tb_url_t[2]
            con = httplib.HTTPConnection(host)
            con.request("POST", path, enc_params, headers)
            r = con.getresponse()
            http_response = r.status
            http_reason = r.reason
            resp = r.read()
            socket.setdefaulttimeout(oldtimeout)
    
            err_code_pat = re.compile("<error>(.*?)</error>",re.DOTALL)
            message_pat = re.compile("<message>(.*?)</message>",re.DOTALL)
            error_code = 0
            message = ""
            err_m = err_code_pat.search(resp)
            if err_m:
                try:
                    error_code = int(err_m.group(1))
                except:
                    pass
            else:
                error_code = 1
            mes_m = message_pat.search(resp)
            if mes_m:
                try:
                    message = mes_m.group(1)
                except:
                    pass
        except Exception,e:
            error_code = -1
            message = str(e)
            log( 'COREBlog2Tool/sendTrackback: '
                     'Some exception occured, %s' % e )
        return error_code,message

    security.declarePublic('discoverTrackback')
    def discoverTrackback(self,url):
        """
        Parse trackback:ping url from given url
        """
        
        o = urllib.urlopen(url)
        src = o.read()
        #Regex pattern
        rdfpat = re.compile("<rdf:RDF.*?</rdf:RDF>",re.DOTALL)
        #Pattern for Trackback PING URL
        tppat = re.compile("""trackback:ping="([^"]+)""",re.DOTALL)
        trackback_ping_url = ""
        #Finc Trackback PING URL
        for item in rdfpat.findall(src):
            m = tppat.search(item)
            if m:
                trackback_ping_url =  m.group(1)
                break
        
        return trackback_ping_url

    
    security.declarePublic('guess_encode')
    def guess_encode(self,s):
        """
        Guess encodings.
        possible_encodings should be set in conf file.
        """
        possible_encodings = ['utf-8','euc_jp','shift-jis','us-ascii']
        guessed_enc = 'us-ascii'
        for enc in possible_encodings:
            try:
                unicode(s,enc)
                guessed_enc = enc
                break;
            except:
                pass
        return guessed_enc

    security.declarePublic('convert_charcode')
    def convert_charcode(self,s,fromcodestr=""):
        """
        convert charcode (for Japanese)
        """
        if type(s) == type(u''):
            #unicode -> str
            s = s.encode('utf-8')
            fromcodestr = code_utf8

        retstr = s

        try:
            import pykf
            pykf_fromcodemap = { \
                pykf.EUC : "euc-jp",
                pykf.SJIS: "shift_jis",
                pykf.UTF8: "utf-8",
                pykf.JIS : "iso-2022-jp" }
            pkf_fromcode = 0
            if not fromcodestr:
                #fromcode is unknown... so do 'guess'
                fromcodestr = self.guess_encode(s)

            #Do conversion...
            retstr = unicode(s, fromcodestr, "replace").encode('utf8')
        except:
            pass
        return retstr

    security.declarePublic('send_mail')
    def send_mail(self, body,to_addr,from_addr,subject):
        #
        # Method to bypass Zope's security.
        # For case of comment/trackback post by anonymous user
        #
        try:
            self.MailHost.send(body, to_addr, from_addr, subject)
        except Exception,e:
            self.MailHost.send(body.encode('utf-8'),
                               to_addr, from_addr,
                               subject.encode('utf-8'))
            log( 'COREBlog2/send_mail: '
                     'Some exception occured, %s' % e )


InitializeClass(COREBlog2Tool)

