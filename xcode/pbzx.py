# Copyright (c) 2017  Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import print_function
import os
import requests
import six
import zipfile

system = require('./system')

url = 'https://github.com/NiklasRosenstein/pbzx/releases/download/v1.0.2/pbzx-1.0.2.zip'

def find_or_install():
  download_dir = os.path.join(__directory__, '_download')
  os.environ['PATH'] = download_dir + os.pathsep + os.environ['PATH']
  try:
    version = system.getoutput('pbzx', '-v')
    return
  except (OSError, system.ExitError) as exc:
    pass

  print('pbzx not available, downloading from', url, '...')
  fp = six.BytesIO(requests.get(url).content)
  archive = zipfile.ZipFile(fp)
  archive.extract('pbzx', download_dir)
  system.call('chmod', '+x', os.path.join(download_dir, 'pbzx'))
  system.getoutput('pbzx', '-v')
