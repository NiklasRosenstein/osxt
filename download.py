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

import click
import getpass
import requests
import posixpath
import re
import sys

index = require('./index')
main = require('./cli').main


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


@main.command()
@click.argument('url', required=False)
def download(url):
  """
  Download a file from the Apple Developer Downloads Center. If no *url*
  is specified, a list of the available downloads will be displayed.
  """

  session = requests.Session()
  apple_id = input('Apple ID: ')
  password = getpass.getpass('Password: ')

  downloads = apple_id_login(session, apple_id, password, getdownloads=not url)
  if downloads is False:
    print('Login failed.')
    sys.exit(1)

  if not url:
    # Filter out the XCode Developer Tools.
    xcode_tools = []
    for data in sorted(downloads['downloads'], key=lambda x: x['dateCreated']):
      if 'xcode' not in data['name'].lower(): continue
      # Find the .dmg image file in the downloadable files.
      for filedata in data['files']:
        if '.dmg' in filedata['remotePath']:
          break
      else:
        continue
      xcode_tools.append({'name': data['name'], 'path': filedata['remotePath']})

    file = index.select_file(xcode_tools, key=lambda x: x['name'])
    url = 'http://adcdownload.apple.com' + file['path']
    print('Download URL:', url)

  response = session.get(url, stream=True)
  filename = re.findall("filename=(\S+)", response.headers.get('Content-Disposition', ''))
  if filename:
    filename = filename[0]
  else:
    filename = posixpath.basename(url)
  size = int(response.headers['Content-Length'])
  bytes_read = 0

  def update():
    p = float(bytes_read) / size * 100
    print("\rDownloading '{}' ... ({}/{}) {}%".format(filename, bytes_read, size, p), end='')
  update()
  with open(filename, 'wb') as fp:
    for data in response.iter_content(4098):
      bytes_read += len(data)
      fp.write(data)
      update()
  print()
