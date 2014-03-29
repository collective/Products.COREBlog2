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
"""COREBlog2 ZConfig loader

"""
__author__  = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'

import os

from ZConfig.loader import ConfigLoader
from Globals import INSTANCE_HOME
from Products.COREBlog2.configuration.schema import coreblog2Schema

# directories
INSTANCE_ETC = os.path.join(INSTANCE_HOME, 'etc')
_here = os.path.dirname(__file__)
COREBLOG2_HOME = os.path.dirname(os.path.abspath(os.path.join(_here)))
COREBLOG2_ETC = os.path.join(COREBLOG2_HOME, 'etc')

# files
CONFIG_NAME = 'coreblog2.conf'
INSTANCE_CONFIG = os.path.join(INSTANCE_ETC, CONFIG_NAME)
COREBLOG2_CONFIG = os.path.join(COREBLOG2_ETC, CONFIG_NAME)
COREBLOG2_CONFIG_IN = os.path.join(COREBLOG2_ETC, CONFIG_NAME+'.in')

# check files for existence
if not os.path.isfile(INSTANCE_CONFIG):
    INSTANCE_CONFIG = None

if not os.path.isfile(COREBLOG2_CONFIG):
    COREBLOG2_CONFIG = None

if not os.path.isfile(COREBLOG2_CONFIG_IN):
    raise RuntimeError("Unable to find configuration file at %s" % 
                        COREBLOG2_CONFIG_IN)
FILES = (INSTANCE_CONFIG, COREBLOG2_CONFIG, COREBLOG2_CONFIG_IN,)

# config
zconf, handler, conf_file = None, None, None
def loadConfig(files, schema=coreblog2Schema, overwrite=False):
    """Config loader
    
    The config loader tries to load the first existing file
    """
    global zconf, handler, conf_file
    if not isinstance(files, (tuple, list)):
        files = (files, )
    if zconf is not None and not overwrite:
        raise RuntimeError, 'Configuration is already loaded'
    for file in files:
        if file is not None:
            if not os.path.exists(file):
                raise RuntimeError, '%s does not exist' % file
            conf_file = file
            zconf, handler = ConfigLoader(schema).loadURL(conf_file)
            break


loadConfig(FILES)

__all__ = ('zconf', 'handler', 'conf_file')
