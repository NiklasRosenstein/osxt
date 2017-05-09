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
from six.moves import input
import click
import glob
import os
import sys

installer = require('./')
system = require('./system')
pbzx = require('./pbzx')


def exit(*message, **kwargs):
    code = kwargs.get('code', 0)
    for key in kwargs:
        raise TypeError("unexpected keyword argument '%s'" % key)
    print(sys.argv[0], '***', *message, file=sys.stderr)
    sys.exit(code)


@click.group()
def main():
    pass


@main.command()
@click.argument('dmg')
@click.argument('dest')
@click.option('-u', '--user', help='THe name of the user that should be '
    'granted ownership of the extracted files. This argument should be '
    'specified when running as superuser.')
@click.option('--debug-pkg', is_flag=True, help='Enter a bash console after '
    'the disk image was mounted and the contained .pkg file is unpacked. '
    'This option was useful during the development, and I figured I\'d not '
    'remove them in case newer versions of the XCode Command-line Tools '
    'have yet again a different structure that needs to be debugged.')
@click.option('--extract', multiple=True, help='One or more files to '
    'extract. Other files will not be extracted if this option is specified.')
def install(dmg, dest, user, debug_pkg, extract):
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
    if os.getuid() != 0:
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

            system.call('rm', '-r', dest)
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
            installer.install_pkg(pkg, dest, extract)

    # Copy the activate script to the destination directory.
    activate_script = os.path.join(__directory__, 'templates', 'activate')
    try:
        system.call('cp', activate_script, os.path.join(dest, 'activate'))
    except system.ExitError as exc:
        print("failed to copy activate script.")

    # Chown the complete destination directory.
    if user:
        installer.chown_recurse(dest, uid, gid)

    return 0


@main.command()
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
    system.call('chmod', '+x', clang_bin)
    system.call(clang_bin, '--version')


if require.main == module:
  main()
