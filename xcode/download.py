# Copyright (C) 2017 Niklas Rosenstein
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
