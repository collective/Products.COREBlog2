##############################################################################
#
# coreblog2testcase.py
# Skelton Class for COREBlog2 Folder
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
#$Id: coreblog2testcase.py 96 2005-11-27 16:38:04Z ats $
#
##############################################################################

"""COREBlog2 tests
"""

__author__  = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'

from Testing import ZopeTestCase
from Products.CMFPlone.tests import PloneTestCase
from Acquisition import aq_base
from DateTime import DateTime

from Products.PloneTestCase import PloneTestCase

PloneTestCase.installProduct('COREBlog2')
PloneTestCase.setupPloneSite(products=['COREBlog2'])

blog_id = 'blog'

entry_body = """
Header
======

Text, text, text

* List
* List
"""

entry_data = (
(entry_body,['cat1'],'2004/10/12'), #0
(entry_body,['cat2'],'2004/10/13'), #1
(entry_body,['cat3'],'2004/10/14'), #2
(entry_body,['cat4'],'2004/9/15'), #3
(entry_body,['cat1'],'2004/8/16'), #4
(entry_body,['cat2'],'2099/1/10'), #5
)

class COREBlog2TestCase(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        # Create a COREBlog2 folder
        self.folder.invokeFactory('COREBlog2', id=blog_id)
        self.failUnless(hasattr(aq_base(self.folder), blog_id))
        self.blog = self.folder[blog_id]


    def makeEntries(self):
        #Test for adding category
        ZopeTestCase._print('Try to add categories ... \n')
        catf = self.blog.getCategoryFolder()
        cat_names = [ 'cat%d' % x for x in range(1,10) ]
        for catname in cat_names:
            catf.invokeFactory('COREBlogCategory',id=catname)
        #Test for category creation
        for catname in cat_names:
            self.failUnless(hasattr(catf, catname),
                        'Category %s not found' %catname)

        #Try to add entry
        ZopeTestCase._print('Try to add entries ... \n')
        cfold = self.blog.getCategoryFolder()
        for cnt in range(0,len(entry_data)):
            new_id = 'entry_%d' % cnt
            self.blog.invokeFactory('COREBlogEntry',new_id)
            self.failUnless(hasattr(self.blog, new_id),
                        'Entry %s not found' %catname)
            ent = self.blog[new_id]
            ent.setBody(entry_data[cnt][0],mimetype='text/structured')
            ent.setEntry_categories(\
                [str(cfold[x].getInternal_id()) for x in entry_data[cnt][1]])
            ent.setEffectiveDate(DateTime(entry_data[cnt][2]))
            ent.indexObject()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(COREBlog2Test))
    return suite

if __name__ == '__main__':
    framework()
