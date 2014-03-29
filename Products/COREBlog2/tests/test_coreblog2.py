##############################################################################
#
# test_coreblog2.py
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
#$Id: test_coreblog2.py 189 2006-04-04 11:32:56Z ats $
#
##############################################################################

"""COREBlog2 tests
"""

__author__  = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'

from Testing import ZopeTestCase
from DateTime import DateTime

from Products.COREBlog2.config import comment_folder_id,catetory_folder_id,\
                stuff_folder_id,images_folder_id


from coreblog2testcase import COREBlog2TestCase
klasses = []

class COREBlog2FolderTest(COREBlog2TestCase): 

    def test_000folders(self):
        #Test for standard folders existance
        ZopeTestCase._print('Test for standard folders ... \n')

        self.failUnless(comment_folder_id in self.blog.objectIds())
        self.failUnless(catetory_folder_id in self.blog.objectIds())
        self.failUnless(stuff_folder_id in self.blog.objectIds())
        self.failUnless(images_folder_id in self.blog.objectIds())

    def test_010catalogqueries(self):
        #Test for catalog queries
        self.makeEntries()
        #Recent entries
        entries = self.blog.getRecentEntry(type=1,limit=5,full_objects=True)
        test_eids = ['entry_%d' % x for x in (2,1,0)]
        self.failUnless([x.id for x in entries] == test_eids,
                            'Wrong order for entry limit in date')

        entries = self.blog.getRecentEntry(type=2,limit=5,full_objects=True)
        test_eids = ['entry_%d' % x for x in (2,1,0,3,4)]
        self.failUnless([x.id for x in entries] == test_eids,
                            'Wrong order for entry limit in count')

        #Entries in month
        entries = self.blog.getEntryInDate(year=2004,month=10,full_objects=True)
        test_eids = ['entry_%d' % x for x in (0,1,2)]
        self.failUnless([x.id for x in entries] == test_eids,
                            'Wrong order for entry in month')

        #Entries in date
        entries = self.blog.getEntryInDate(year=2004,month=9,day=15,
                                                    full_objects=True)
        test_eids = ['entry_%d' % x for x in (3,)]
        self.failUnless([x.id for x in entries] == test_eids,
                            'Wrong order for entry in month')

        #Previous entry
        entries = self.blog.getNearestEntry(base_date='2004/9/15')
        self.failUnless(entries[1].id == 'entry_4',
                            'Wrong entry,previous')

        #Next entry
        entries = self.blog.getNearestEntry(base_date='2004/9/15',
                                            sort_order='normal')
        self.failUnless(entries[1].id == 'entry_0',
                            'Wrong entry,next')

        #Entries in category
        cfold = self.blog.getCategoryFolder()
        entries = self.blog.getEntryInCategory(\
                        category_ids=[cfold['cat1'].getInternal_id(),])
        self.failUnless(len(entries[0]) != 2,
                            'Wrong entry number in cat1')
        self.failUnless(entries[0].id == 'entry_4',
                            'Wrong entry in cat1')
        self.failUnless(entries[1].id == 'entry_0',
                            'Wrong entry in cat1')

klasses.append(COREBlog2FolderTest)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    for klass in klasses:
        suite.addTest(makeSuite(klass))
    return suite

if __name__ == '__main__':
    framework()
