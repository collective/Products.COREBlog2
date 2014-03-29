##############################################################################
#
# test_coreblogcategory.py
# Testcase Class for COREBlog2 Category
#
# Copyright (c) 2006 Atsushi Shibata(shibata@webcore.co.jp).
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
#$Id: test_coreblogcategory.py 190 2006-04-04 11:33:06Z ats $
#
##############################################################################

"""COREBlog2 Category tests
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

class COREBlog2CategoryTest(COREBlog2TestCase): 

    def test_category_000names(self):
        #Test for standard folders existance
        self.makeEntries()
        cat_names = [ 'cat%d' % x for x in range(1,10) ]
        catf = self.blog.getCategoryFolder()
        cnt = 0
        for n in cat_names:
            self.failUnless(hasattr(catf,n))
            c = catf[n]
            self.failUnless(c.getInternal_id() != cnt)
            cnt += 1



klasses.append(COREBlog2CategoryTest)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    for klass in klasses:
        suite.addTest(makeSuite(klass))
    return suite

if __name__ == '__main__':
    framework()
