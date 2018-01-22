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

import argparse
import bs4, html5lib
import os
import sys

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

mkiso_parser = subparsers.add_parser('mkiso', description='''
  Build an .ISO image from an OSX installer application. Such an installer
  application can be downloaded from the App Store, eg. "Install macOS Sierra.app".
''')
mkiso_parser.add_argument('installer', nargs='?')
mkiso_parser.add_argument('-o', '--output', help='Name of the output ISO file.')

vbx_parser = subparsers.add_parser('vbx', description='''
  Create and/or configure a VirtualBox virtual machine for the installation
  of a macOS image. Setting up a new macOS virtual machine has never been
  easier (works on all host systems).

  To create a new macOS virtual machine, first create a new OSX ISO image
  using the `osxt mkiso` command. Then use this command to set up a new
  machine, for example:

      osxt vbx "macOS Sierra" --new --image ./macOS-Sierra.img
''')
vbx_parser.add_argument('vm_name', help='The name of the VirtualBox machine to create or modify.')
vbx_parser.add_argument('--new', action='store_true', help='Create a new VM. Implies --all.')
vbx_parser.add_argument('--all', action='store_true', help='Perform all configuration steps.')
vbx_parser.add_argument('--general', action='store_true', help='Perform general configuration steps, such as memory, vram, cpu count, firmware, etc.')
vbx_parser.add_argument('--storage', action='store_true', help='Set up storage configuration.')
vbx_parser.add_argument('--image', help='Disk image to attach. Implies --storage.')
vbx_parser.add_argument('--device', help='Configure a specific host device. If --all is used, the default device is MacBookPro11,3.')
vbx_parser.add_argument('--list-devices', action='store_true', help='List available host devices for which a --device-serial can be automatically selected.')
vbx_parser.add_argument('--device-serial', help='Manually specify the device serial number. Must be paired with a --device name.')
vbx_parser.add_argument('--cpu', help='Manually specify the CPU ID set. This option is not automatically used with --all but defaults to IvyBridge-0 when --new is used.')
vbx_parser.add_argument('--list-cpus', help='List available CPU ID sets.')
vbx_parser.add_argument('--resolution', help='Set the display resolution. Must be an integer between 0 and 5, referring to 640x480, 800x600, 1024x768, 1280x1024, '
    '1440x900 and 1920x1200 respectively. This option is not automatically implied with --all, but --new specifies a default of 4 (1440x900)')

vbm_parser = subparsers.add_parser('vbm', description='''
  Shorthand for VBoxManage. Useful on Windows when VirtualBox is not on the PATH.
''')
vbm_parser.add_argument('argv', nargs='...')


xcode_parser = subparsers.add_parser('xcode')
xcode_subparser = xcode_parser.add_subparsers(dest='xcode_command')

xcode_install_parser = xcode_subparser.add_parser('install', description='''
  Install macOS XCode command-line tools from a Disk Image File (.dmg).
  Must be run as a superuser if you want to install macOS SDK components.
''')
xcode_install_parser.add_argument('dmg', help='Path to the Disk Image file. The XCode command-line tools .dmg files can be downloaded from the '
    'Apple Developer Portal: https://developer.apple.com/downloads/index.action')
xcode_install_parser.add_argument('directory', help='The directory where the XCode command-line tools will be installed to.')
xcode_install_parser.add_argument('-u', '--user', help='The name of the user that should be granted ownership of the extracted files. This argument '
    'should be specified when running as a superuser.')
xcode_install_parser.add_argument('--debug-pkg', action='store_true', help='Enter an interactive bash session after the disk image was mounted and the contained '
    '.pkg file was extracted. This option is useful when the installation process fails to inspect the contents of the .pkg file.')

xcode_getversion_parser = xcode_subparser.add_parser('getversion', description='''
  Installs to a temporary directory and outputs the clang version, then
  removes the temporarily installed files again.
''')
xcode_getversion_parser.add_argument('dmg')
xcode_getversion_parser.add_argument('-v', '--verbose')

xcode_download_parser = xcode_subparser.add_parser('download', description='''
  Download a file from the Apple Developer Portal. If URL is specified, it must
  either be the (partial) name of an XCode Disk Image file as specified in the
  XCode Version Table (see the osxt README file) or a full download URL.

  If no URL is specified, an interactive session will allow you to selected
  a version.
''')
xcode_download_parser.add_argument('url', nargs='?')
xcode_download_parser.add_argument('-l', '--list', action='store_true', help='List the downloads available from the XCode Version Table in the osxt README. '
    'If the URL argument is specified, only results that contain the URL string will be printed.')
xcode_download_parser.add_argument('--show-url', action='store_true', help='Print the download URL when using the --list option.')
xcode_download_parser.add_argument('--apple-id', help='You\'re Apple ID. Will be prompted if not specified.')


def mkiso(args):
  import re
  import system from './system'
  import {MountFile} from './installer'

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

  installer = args.installer
  output = args.output

  if installer and not os.path.isabs(installer) and not os.path.exists(installer):
    installer = os.path.join('/Applications', installer)
  if not installer:
    installer = find_installer_application_path()
    if not installer:
      print('error: OSX installer could not be automatically determined')
      return 1
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
    system.call('hdiutil', 'create', '-o', filename,
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


def vbcall(prog, *args, **kwargs):
  import system from './system'
  if os.name == 'nt' and not os.path.isabs(prog):
    prog = os.path.join('C:\\Program Files\\Oracle\\VirtualBox', prog)
  return system.call(prog, *args, **kwargs)


def vbmanage(*args, **kwargs):
  return vbcall('VBoxManage', *args, **kwargs)


def vbx(args):
  import system from './system'

  # From http://www.insanelymac.com/forum/topic/309654-run-vanilla-os-x-el-capitan-sierra-yosemite-or-mavericks-in-virtualbox-5010-on-a-windows-host/
  DEVICE_SERIALS = {
    'iMac11,3': 'Mac-F2238BAE',
    'MacBookPro11,3': 'Mac-2BD1B31983FE1663',
    'MacMini6,2': 'Mac-F65AE981FFA204ED'
  }
  CPU_IDS = {
    'Lynnfield-i5-750': '00000001 000106e5 06100800 0098e3fd bfebfbff',
    'IvyBridge-0': '00000001 000306a9 04100800 7fbae3ff bfebfbff',
    'IvyBridge-1': '00000001 000306a9 00020800 80000201 178bfbff'
  }

  vm = args.vm_name
  new = args.new
  all = args.all
  storage = args.storage
  image = args.image
  general = args.general
  device = args.device
  device_serial = args.device_serial
  cpu = args.cpu
  resolution = args.resolution

  if args.list_devices:
    for key in DEVICE_SERIALS.keys():
      print(key)
    return 0
  if args.list_cpus:
    for key in CPU_IDS:
      print(key)
    return 0

  if device and device not in device_serials and not device_serial:
    print('error: unknown device: {!r}')
    print('error: add --device-serial to manually specify the serial number')
    return 1
  if device_serial and not device:
    print('error: missing --device option with --device-serial is specified')
    return 1
  if new and not cpu:
    cpu = 'IvyBridge-0'
  if cpu:
    parts = cpu.split(' ')
    if len(parts) != 5 or not all(len(x) == 8 for x in parts):
      if cpu not in CPU_IDS:
        print('error: invalid CPU ID: {!r}'.format(cpu))
        return 1
      cpu = CPU_IDS[cpu]
  if resolution and resolution not in ('0', '1', '2', '3', '4', '5'):
    print('error: invalid resolution: {!r}'.format(resolution))
    return 1
  if new and not resolution:
    resolution = '4'

  if new:
    all = True
    vbmanage('createvm', '--name', vm, '--ostype', 'MacOS_64', '--register')
  if storage or all:
    vbmanage('storagectl', vm, '--name', 'SATA Controller', '--add', 'sata', '--controller', 'IntelAHCI')
    if image:
      vbmanage('storageattach', vm, '--storagectl', 'SATA Controller', '--port',
        '0', '--device', '0', '--type', 'hdd', '--medium', os.path.abspath(image))
  elif image:
    print('warning: --image only with --storage')
  if general or all:
    options = (
      '--audiocontroller hda '
      '--chipset ich9 '
      '--firmware efi '
      '--cpus 2 '
      '--hpet on '
      '--keyboard usb '
      '--memory 4096 '
      '--mouse usbtablet '
      '--vram 128 '
    ).split()
    vbmanage('modifyvm', vm, *options)
  if cpu:
    vbmanage('modifyvm', vm, '--cpuidset', *cpu.split(' '))
  if device or all:
    if not device:
      device = 'MacBookPro11,3'
    if not device_serial:
      device_serial = DEVICE_SERIALS[device]
    vbmanage('setextradata', vm, 'VBoxInternal/Devices/efi/0/Config/DmiSystemProduct', device)
    vbmanage('setextradata', vm, 'VBoxInternal/Devices/efi/0/Config/DmiSystemVersion', '1.0')
    vbmanage('setextradata', vm, 'VBoxInternal/Devices/efi/0/Config/DmiBoardProduct', device_serial)
    vbmanage('setextradata', vm, 'VBoxInternal/Devices/smc/0/Config/DeviceKey',
      'ourhardworkbythesewordsguardedpleasedontsteal(c)AppleComputerInc')
    vbmanage('setextradata', vm, 'VBoxInternal/Devices/smc/0/Config/GetKeyFromRealSMC', '1')
  if resolution:
    vbmanage('setextradata', vm, 'VBoxInternal2/EfiGopMode', resolution)


def xcode(args):
  global getpass, glob, requests, posixpath, installer, system, pbzx
  import getpass
  import glob
  import requests
  import posixpath
  import installer from './installer'
  import system from './system'
  import pbzx from './pbzx'

  if args.xcode_command == 'install':
    return xcode_install(args)
  elif args.xcode_command == 'getversion':
    return xcode_getversion(args)
  elif args.xcode_command == 'download':
    return xcode_download(args)
  else:
    print('error: unexpected subcommand: {!r}'.format(args.xcode_command))


def xcode_install(args):
  dmg = args.dmg
  dest = args.directory
  user = args.user
  debug_pkg = args.debug_pkg

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
  activate_script = str(module.directory.joinpath('../templates/activate'))
  try:
    system.call('cp', activate_script, os.path.join(dest, 'activate'))
  except system.ExitError as exc:
    print("failed to copy activate script.")

  # Chown the complete destination directory.
  if user:
    system.call('chown', '-R', user, dest)

  return 0


def xcode_getversion(args):
  dmg = args.dmg
  system.verbose = args.verbose
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


def xcode_download(args):
  import {apple_id_login, parse_xcode_version_table} from './download'
  from prompt_toolkit import prompt
  from prompt_toolkit.contrib.completers import WordCompleter

  url = args.url
  list = args.list
  apple_id = args.apple_id
  show_url = args.show_url

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
  apple_id = apple_id or input('Apple ID: ')
  password = getpass.getpass('Password: ')

  if not apple_id_login(session, apple_id, password):
    print('Login failed.')
    sys.exit(1)

  response = session.get(url, stream=True)
  response.raise_for_status()
  if 'Content-Length' in response.headers:
    size = int(response.headers['Content-Length'])
  else:
    size = None
  bytes_read = 0

  if response.headers['Content-Type'] == 'text/html':
    soup = bs4.BeautifulSoup(response.content, 'html5lib')
    print(soup.find(id='content'))
    return 1

  # TODO: Nicer progress bar.
  def update():
    print('\rDownloading \'{}\' ... ({}/{})'.format(filename, bytes_read, size), end='')
    if size:
      p = float(bytes_read) / size * 100
      print(' {}%'.format(p), end='')
  update()
  with open(filename, 'wb') as fp:
    for data in response.iter_content(4098):
      bytes_read += len(data)
      fp.write(data)
      update()
  print()


def main(argv=None):
  args = parser.parse_args(argv)
  if args.command == 'mkiso':
    return mkiso(args)
  elif args.command == 'vbx':
    return vbx(args)
  elif args.command == 'vbm':
    return vbmanage(*args.argv)
  elif args.command == 'xcode':
    return xcode(args)
  else:
    parser.print_usage()
    return 0


if require.main == module:
  sys.exit(main())
