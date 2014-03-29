##############################################################################
#
# test_coreblogentry.py
# Testcase Class for COREBlog2 Folder
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
#$Id: test_coreblogentry.py 94 2005-11-27 16:37:14Z ats $
#
##############################################################################

"""COREBlog2 Entry tests
"""

__author__  = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'

from Testing import ZopeTestCase
from DateTime import DateTime

from Products.COREBlog2.config import comment_folder_id,catetory_folder_id,\
                stuff_folder_id,images_folder_id

from Products.COREBlog2.content.coreblogentry import COREBlogEntry


from coreblog2testcase import COREBlog2TestCase
klasses = []

class COREBlog2EntryTest(COREBlog2TestCase): 

    def test_addcomments(self):
        #Test for standard folders existance
        self.makeEntries()
        baseentry = self.blog['entry_3']
        #Previous entry
        entry = baseentry.getPreviousEntry()
        self.failUnless(entry.id == 'entry_4',
                            'Wrong entry,previous')
        #Next entry
        entry = baseentry.getNextEntry()
        self.failUnless(entry.id == 'entry_0',
                            'Wrong entry,next')
        baseentry = self.blog['entry_2']
        entry = baseentry.getNextEntry()
        self.failUnless(entry == None,
                            'Wrong entry,next')

        #Test for add comments
        baseentry = self.blog['entry_3']
        baseentry.addComment2Entry(author='name0',email='email@com',
                    url='http://foo.bar/0',title='title0',body='body0')
        baseentry.addComment2Entry(author='name1',email='email@com',
                    url='http://foo.bar/1',title='title1',body='body1')
        self.failUnless(baseentry.countComment() == 2,
                            'Wrong comment number')

        #Try to add comment on closed entry.
        baseentry = self.blog['entry_4']
        baseentry.setAllow_comment(COREBlogEntry.comment_none)
        baseentry.addComment2Entry(author='name0',email='email@com',
                    url='http://foo.bar/0',title='title0',body='body0')
        self.failUnless(baseentry.countComment() == 0,
                            'Wrong comment number for comment setting "none"')

        baseentry.setAllow_comment(COREBlogEntry.comment_closed)
        baseentry.addComment2Entry(author='name0',email='email@com',
                    url='http://foo.bar/0',title='title0',body='body0')
        self.failUnless(baseentry.countComment() == 0,
                            'Wrong comment number for comment setting "closed"')


        #Test for add trackbacks
        baseentry = self.blog['entry_2']
        baseentry.addTrackback2Entry(blog_name='name0',url='http://foo.bar/0',
                                title='title0',excerpt='body0')
        baseentry.addTrackback2Entry(blog_name='name1',url='http://foo.bar/1',
                                title='title1',excerpt='body1')
        self.failUnless(baseentry.countTrackback() == 2,
                            'Wrong trackback number')

        #Try to add trackback on closed entry.
        baseentry = self.blog['entry_0']
        baseentry.setAllow_comment(COREBlogEntry.trackback_none)
        baseentry.addTrackback2Entry(blog_name='name0',url='http://foo.bar/0',
                                title='title0',excerpt='body0')
        self.failUnless(baseentry.countComment() == 0,
                            'Wrong trackback number for comment setting "none"')

        baseentry.setAllow_comment(COREBlogEntry.trackback_closed)
        baseentry.addTrackback2Entry(blog_name='name0',url='http://foo.bar/0',
                                title='title0',excerpt='body0')
        self.failUnless(baseentry.countComment() == 0,
                        'Wrong trackback number for comment setting "closed"')

klasses.append(COREBlog2EntryTest)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    for klass in klasses:
        suite.addTest(makeSuite(klass))
    return suite

if __name__ == '__main__':
    framework()
