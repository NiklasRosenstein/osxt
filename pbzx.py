# Copyright (C) 2014-2017 Niklas Rosenstein
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

from __future__ import print_function
from six.moves.urllib.request import urlopen
import os
import six
import zipfile

system = require('./system')

url = 'https://github.com/NiklasRosenstein/pbzx/releases/download/v1.0.2/pbzx-1.0.2.zip'

def find_or_install():
  download_dir = os.path.join(__directory__, '_download')
  os.environ['PATH'] = download_dir + os.pathsep + os.environ['PATH']
  try:
    version = system.getoutput('pbzx', '-v')
  except (OSError, system.ExitError) as exc:
    pass
  else:
    print(version)
    return

  print('pbzx not available, downloading from', url, '...')
  fp = six.BytesIO(urlopen(url).read())
  archive = zipfile.ZipFile(fp)
  archive.extract('pbzx', download_dir)
  system.call('chmod', '+x', os.path.join(download_dir, 'pbzx'))
  system.getoutput('pbzx', '-v')
