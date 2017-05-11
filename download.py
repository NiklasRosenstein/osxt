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

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter

import click
import getpass
import os
import posixpath
import re
import requests
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


@main.command()
@click.argument('url', required=False)
def download(url):
  """
  Download a file from the Apple Developer Downloads Center.

  If URL is specified, it must either be the (partial) name of an XCode
  Disk Image file as specified in the XCode Version Table in the readme
  of XCode CLTools Installer, or otherwise a full download URL.

  If URL is not specified, an interactive terminal UI will allow you to
  select the a version.
  """

  if not url or not url.startswith('http'):
    versions = parse_xcode_version_table()
    if url:
      results = []
      for v in versions:
        if v[0].startswith(url):
          results.append(v)
      if len(results) == 0:
        print('error: no versions matching "{}"'.format(url))
        sys.exit(1)
      elif len(results) > 1:
        print('error: multiple versions matching "{}"'.format(url))
        sys.exit(1)
      filename, url = results[0]
    else:
      choices = [x[0] for x in versions]
      choice = prompt('Disk Image: ', completer=WordCompleter(choices, sentence=True))
      if choice not in choices:
        print('error: invalid selection "{}"'.format(url))
        sys.exit(1)
      filename, url = versions[choices.index(choice)]
  else:
    filename = posixpath.basename(url)

  session = requests.Session()
  apple_id = input('Apple ID: ')
  password = getpass.getpass('Password: ')

  if not apple_id_login(session, apple_id, password):
    print('Login failed.')
    sys.exit(1)

  response = session.get(url, stream=True)
  size = int(response.headers['Content-Length'])
  bytes_read = 0

  # TODO: Nicer progress bar.
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
