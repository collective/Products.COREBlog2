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
"""COREBlog2 ZConfig schema loader

"""
__author__  = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'

import os

from ZConfig.datatypes import Registry
from ZConfig.loader import SchemaLoader
from Products.COREBlog2.configuration import datatype

# schema file
DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_FILE_NAME = 'schema.xml'
SCHEMA_FILE = os.path.join(DIR, SCHEMA_FILE_NAME)
print SCHEMA_FILE

# schema
coreblog2Schema = None
def loadSchema(file, registry=Registry(), overwrite=False):
    """Loads a schema file
    
    * file
      A path to a file
    * registry
      A ZConfig datatypes registry instance
    * overwrite
      Overwriting the existing global schema is not possible unless overwrite
      is set to true. Useful only for unit testing.
    """
    global coreblog2Schema
    if coreblog2Schema is not None and not overwrite:
        raise RuntimeError, 'Schema is already loaded'
    schemaLoader = SchemaLoader(registry=registry)
    coreblog2Schema = schemaLoader.loadURL(file)
    return coreblog2Schema

loadSchema(SCHEMA_FILE)

__all__ = ('coreblog2Schema',)
