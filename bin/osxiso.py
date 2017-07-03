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

import click
import os
import re
import {main} from './main'
import system from  '../xcode/system'
import {MountFile} from '../xcode/installer'


def find_installer_application_path():
  choices = [
    'Install macOS Sierra.app',
    'Install OS X El Capitan.app',
    'Install OS X Yosemite.app'
  ]
  for app in choices:
    path = os.path.join('/Applications', app)
    if os.path.isdir(path):
      return path
  return None


def create_iso():
  pass


@main.command()
@click.argument('installer', required=False)
@click.option('-o', '--output', help='Output ISO image name.')
def osxiso(installer, output):
  " Generate a macOS ISO image file. "

  if installer and not os.path.isabs(installer) and not os.path.exists(installer):
    installer = os.path.join('/Applications', installer)
  if not installer:
    installer = find_installer_application_path()
  if not output:
    base = os.path.splitext(os.path.basename(installer))[0]
    if base.startswith('Install'):
      base = base[8:]
    base = re.sub('\s+', '-', base)
    output = base + '.iso'

  fn = os.path.join(installer, 'Contents/SharedSupport/InstallESD.dmg')
  args = ['-noverify', '-nobrowse']
  with MountFile(fn, args) as mount:
    filename = '/tmp/' + os.path.basename(output)
    # Create a blank ISO image with a single partition map.
    system.call('hdiutil', 'create', '-o', filename, '-size', '8g',
      '-layout', 'SPUD', '-fs', 'HFS+J', '-type', 'SPARSE')
    # Mount the sparse bundle for package addition.
    system.call('hdiutil', 'attach', filename + '.sparseimage', '-noverify',
      '-nobrowse', '-mountpoint', '/Volumes/install_build')
    # Restore the base system into the ISO image.
    # Mounts "OS X Base System".
    system.call('asr', 'restore', '-source', os.path.join(mount, 'BaseSystem.dmg'),
      '-target', '/Volumes/install_build', '-noprompt', '-noverify', '-erase')
    # Remove package link and replace with actual files.
    system.call('rm', '/Volumes/OS X Base System/System/Installation/Packages')
    system.call('cp', '-rp', os.path.join(mount, 'Packages'),
      '/Volumes/OS X Base System/System/Installation')
    # Copy installer dependencies.
    system.call('cp', '-rp', os.path.join(mount, 'BaseSystem.chunklist'),
      '/Volumes/OS X Base System/BaseSystem.chunklist')
    system.call('cp', '-rp', os.path.join(mount, 'BaseSystem.dmg'),
      '/Volumes/OS X Base System/BaseSystem.dmg')

  system.call('hdiutil', 'detach', '/Volumes/OS X Base System')
  # Optimise Sparseimage size.
  system.call('hdiutil', 'compact', filename + '.sparseimage', '-batteryallowed')
  system.call('hdiutil', 'resize', '-size', 'min', filename + '.sparseimage')
  # Convert the sparseimage to ISO.
  system.call('hdiutil', 'convert', filename + '.sparseimage',
    '-format', 'UDTO', '-o', filename)

  print('Moving {} to {} ...'.format(filename, output))
  os.rename(filename + '.cdr', output)
  os.remove(filename + '.sparseimage')
