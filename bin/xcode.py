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

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter

import click
import getpass
import glob
import requests
import os
import posixpath
import sys
import {main} from '../bin/main'
import installer from '../xcode/installer'
import system from '../xcode/system'
import pbzx from '../xcode/pbzx'
import {apple_id_login, parse_xcode_version_table} from '../xcode/download'


def exit(*message, **kwargs):
    code = kwargs.get('code', 0)
    for key in kwargs:
        raise TypeError("unexpected keyword argument '%s'" % key)
    print(sys.argv[0], '***', *message, file=sys.stderr)
    sys.exit(code)


@main.group()
def xcode():
    " Download and install XCode CommandLine Tools. "
    pass


@xcode.command()
@click.argument('dmg')
@click.argument('dest')
@click.option('-u', '--user', help='The name of the user that should be '
    'granted ownership of the extracted files. This argument should be '
    'specified when running as superuser.')
@click.option('--debug-pkg', is_flag=True, help='Enter a bash console after '
    'the disk image was mounted and the contained .pkg file is unpacked. '
    'This option was useful during the development, and I figured I\'d not '
    'remove them in case newer versions of the XCode Command-line Tools '
    'have yet again a different structure that needs to be debugged.')
def install(dmg, dest, user, debug_pkg):
    """
    Create a local installation of the Mac OS Command Line Tools from
    a Disk Image File. For installation that includes the Mac OS SDK
    components, must be run as superuser.

    DMG must be the path to the .dmg file that contains the Mac OS
    Command-line Tools. These can be downloaded from the Apple Developer
    Download:

        https://developer.apple.com/downloads/index.action

    DEST is the path where the Command-line Tools will be extracted to.
    After the extraction is complete, an `activate` script will be created
    that can be sourced from the terminal to get access to the toolchain.

    If `pbzx` is not available on the system, it will be automatically
    downloaded from https://github.com/NiklasRosenstein/pbzx/releases.
    """

    pbzx.find_or_install()

    # If the Mac OS SDK should be installed, this should be run
    # as superuser. Otherwise, some files might not be extracted
    # properly from the archive.
    if os.getuid() != 0 and system.verbose:
        print('warning: not run as superuser, some files might not get extracted')

    if not user:
        user = system.getoutput('logname').strip()

    # Determine the user and group ID of the new user.
    if user:
        try:
            uid = int(system.getoutput('id', '-u', user))
            gid = int(system.getoutput('id', '-g', user))
        except (ValueError, system.ExitError):
            exit('could not determine uid/gid for user', user, code=1)
    else:
        uid = gid = None

    # Make sure the output directory exists, and that it does
    # not already contain any important files.
    if os.path.exists(dest):
        if not os.path.isdir(dest):
            exit("'%s' is not a directory" % dest, code=1)

        if installer.dir_has_contents(dest):
            string = input("'%s' is not empty, it'll be erased. "
                "Okay with that? [yes/no] " % dest).strip().lower()
            if not string or string not in ('yes', 'y'):
                exit('user stop')

            system.call('rm', '-rf', dest)
            system.call('mkdir', dest)
    else:
        system.call('mkdir', '-p', dest)

    # Mount the Disk Image File and search for the CLTools and
    # Mac OS SDK package files.
    packages = None
    with installer.MultiContext() as context:
        volume = context.enter(installer.MountFile(dmg))

        # Two choices: Either, the CLTools and SDK packages are
        # contained in a Packages/ subdirectory or in another
        # Package archive.
        packages_dir = os.path.join(volume, 'Packages')
        if os.path.isdir(packages_dir):
            packages = installer.detect_packages(packages_dir)
        else:
            # So, there must be a *.pkg file in this Disk Image File
            # which in turn contains the CLTools and SDK packages.
            pkgs = glob.glob(os.path.join(volume, '*.pkg'))
            if not pkgs:
                exit('No *.pkg found in Disk Image File', code=1)
            elif len(pkgs) != 1:
                print('Not sure which *.pkg to use from Disk Image File.')
                filename = installer.select_file(pkgs)
            else:
                filename = pkgs[0]

            # We need to unpack the PKG in order to acces its
            # contained packages (the CLTools and SDK packages).
            tmpdir = context.enter(installer.TempDir())
            installer.unpack_pkg(filename, tmpdir)
            packages = installer.detect_packages(tmpdir)

        if debug_pkg:
            olddir = os.getcwd()
            os.chdir(tmpdir)
            try:
                system.call('bash')
            except system.ExitError as exc:
                print('aborted after --debug-pkg')
                return exc.code
            finally:
                os.chdir(olddir)

        for pkg in packages:
            installer.install_pkg(pkg, dest)

    # Copy the activate script to the destination directory.
    activate_script = os.path.join(__directory__, 'templates', 'activate')
    try:
        system.call('cp', activate_script, os.path.join(dest, 'activate'))
    except system.ExitError as exc:
        print("failed to copy activate script.")

    # Chown the complete destination directory.
    if user:
        system.call('chown', '-R', user, dest)

    return 0


@xcode.command()
@click.argument('dmg')
@click.option('-v', '--verbose', is_flag=True)
def getversion(dmg, verbose):
  """
  Installs to a temporary directory and outputs the clang version.
  """

  system.verbose = verbose
  with installer.TempDir() as dir:
    ret = install([dmg, dir], '--extract', '/usr/bin/clang', standalone_mode=False)
    if ret != 0:
        # TODO: Currently extracts all files, but we only need the clang binary.
        print('error: extraction failed', file=sys.stderr)
        return 1
    clang_bin = os.path.join(dir, 'usr/bin/clang')
    if not os.path.isfile(clang_bin):
        clang_bin = os.path.join(dir, 'Library/Developer/CommandLineTools/usr/bin/clang')
    system.call(clang_bin, '--version')


@xcode.command()
def getpbzx():
    """
    Checks if pbzx is available, otherwise download's it from GitHub.
    """

    pbzx.find_or_install()


@xcode.command()
@click.argument('url', required=False)
@click.option('-l', '--list', is_flag=True, help='List the downloads available '
  'from the XCode Version Table that can be found in the README and exit. If '
  'the URL argument is specified, only results that contain the URL string '
  'will be printed.')
@click.option('--show-url', is_flag=True, help='Show the download URL when '
  'listing available versions.')
def download(url, list, show_url):
  """
  Download a file from the Apple Developer Downloads Center.

  If URL is specified, it must either be the (partial) name of an XCode
  Disk Image file as specified in the XCode Version Table in the readme
  of XCode CLTools Installer, or otherwise a full download URL.

  If URL is not specified, an interactive terminal UI will allow you to
  select the a version.
  """

  if list:
    versions = parse_xcode_version_table()
    for version in versions:
        if url and url not in version[0]:
            continue
        if show_url:
            print(version[0], '{' + version[1] + '}')
        else:
            print(version[0])
    return

  if not url or not url.startswith('http'):
    versions = parse_xcode_version_table()
    if url:
      results = []
      for v in versions:
        if url in v[0]:
          results.append(v)
      if len(results) == 0:
        print('error: no versions matching "{}"'.format(url))
        sys.exit(1)
      elif len(results) > 1:
        print('error: multiple versions matching "{}"'.format(url))
        for v in results[:5]:
            print('  -', v[0])
        if len(results) > 5:
            print('  - ...')
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
