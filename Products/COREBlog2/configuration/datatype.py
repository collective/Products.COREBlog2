#  ZConfig loader for COREBlog2,
#  based on ATContentTypes
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU Gefneral Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""COREBlog2 ZConfig datatypes

"""
__author__  = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'

from Products.CMFCore import permissions as CMFCorePermissions
from AccessControl import Permissions as ZopePermissions
from ZConfig.datatypes import IdentifierConversion
from ZConfig.datatypes import stock_datatypes


class BaseFactory(object):
    """Basic factory
    """
    
    def __init__(self, section):
        self.name = section.getSectionName()
        #self._parsed = False
        self._section = section
        self._names = {}
        self._parse()
        
    #def __call__(self):
    #    if not self._parsed:
    #        self._parse()
    #    return self
        
    def set(self, name, value):
        self._names[name] = 1
        setattr(self, name, value)
        
    def _parse(self):
        raise NotImplementedError
        
class COREBlog2(BaseFactory):
    """data handler for a coreblog2
    """
    
    def _parse(self):
        sec = self._section
        
        self.set('ping_timeout_default',sec.ping_timeout_default)
        
        # Settings for COREBlog2
        self.set('top_entry_count_default',sec.top_entry_count_default)
        self.set('portlet_item_count_default',sec.portlet_item_count_default)
        self.set('batch_size_default',sec.batch_size_default)
        self.set('dont_send_ping_default',sec.dont_send_ping_default)
        
        # left_slot
        ct = sec.left_slots_default
        if ct is not None:
            slots = tuple(ct.metal_path)
            self.set('left_slots_default',slots)
        ct = sec.right_slots_default
        if ct is not None:
            slots = tuple(ct.metal_path)
            self.set('right_slots_default',slots)
        
        # Settings for Entry
        self.set('description_length',sec.description_length)
        ct = sec.contenttypes
        if ct is not None:
            allowed = tuple(ct.allowed_content_types)
            self.set('allowed_content_types', allowed)
