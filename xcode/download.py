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

import os
import re


def apple_id_login(session, apple_id, password, getdownloads=False):
  """
  This function performs log-in on the Apple ID page and grabs the
  authentication cookie to be able to download files from the Apple
  Developer Downloads.

  If #getdownloads is #True, a JSON object that contains the available
  download information will be returned, otherwise only the required
  setups are performed. If #getdownloads is #False, #True will be
  returned if the log-in succeeded.

  Returns #False if the log-in failed.
  """

  # Request session cookies.
  session.get('https://idmsa.apple.com/IDMSWebAuth/login?appIdKey=891bd3417'
              'a7776362562d2197f89480a8547b108fd934911bcbea0110d07f757&path'
              '=%2Fdownload%2F&rv=1')

  data = {'appleId': apple_id, 'accountPassword': password}
  response = session.post('https://idmsa.apple.com/IDMSWebAuth/authenticate',
    allow_redirects=False, data=data)

  # We expect a redirect if the log-in succeeds.
  if response.status_code != 302:
    return False

  # Grab the the ADCDownloadAuth cookie.
  response = session.get('https://developer.apple.com/services-account/QH65B2/'
                         'downloadws/listDownloads.action', stream=True)

  if getdownloads:
    return response.json()
  return True


def parse_xcode_version_table():
  """
  Parses the XCode Version Table in the README.md and returns a list of the
  available versions.
  """

  with open(os.path.join(__directory__, 'README.md')) as fp:
    contents = fp.read()

  begin = contents.find('<!-- XCode Version Table Begin -->')
  end = contents.find('<!-- XCode Version Table End -->')
  if begin < 0 or end < 0:
    raise RuntimeError('could not find XCode Version Table in README.md')
  contents = contents[begin:end]
  results = re.findall('\[(xcode(?:[\.\d]+)-.*?.dmg)\]\((.*?)\)', contents)
  return results
