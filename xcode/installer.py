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
import glob
import os
import re
import pipes
import shutil
import subprocess
import sys
import tempfile

system = require('./system')


class TempDir(object):
    '''
    This context-manager creates a temporary directory with
    :meth:`tempfile.mkdtemp` and removes the complete directory
    upon context-exit.

    Alternatively, the folder will be deleted when the TempDir
    object is garbage collected.
    '''

    def __init__(self, delete=True):
        super(TempDir, self).__init__()
        self.delete = delete

    def __del__(self):
        self.__exit__(None, None, None)

    def __enter__(self):
        self.folder = tempfile.mkdtemp()
        return self.folder

    def __exit__(self, *args):
        if self.folder and os.path.isdir(self.folder):
            if self.delete:
                shutil.rmtree(self.folder)
            self.folder = None


class MountFile(object):
    '''
    This context-manager is a utility for mounting Disk Image Files
    using the ``hdiutil`` system command.
    '''

    expr = re.compile('\s+(/Volumes/.*)$', re.M | re.I)

    def __init__(self, filename, args=None):
        super(MountFile, self).__init__()
        self.filename = filename
        self.volume = None
        self.args = [] if args is None else args

    def __enter__(self):
        # Run the hdiutil command to mount the file and determine
        # the Volume at which it was mounted.
        try:
            output = system.getoutput('hdiutil', 'mount', self.filename, *self.args)
        except system.ExitError:
            raise RuntimeError("could not found '%s'" % self.filename)

        # Find the name of the volume in the output.
        volume = self.expr.search(output)
        if not volume:
            raise RuntimeError("could not determine mount volume for '%s'"
                % self.filename)

        self.volume = volume.group(1).strip()
        return self.volume

    def __exit__(self, *args):
        # Unmount the volume if it was mounted before.
        if self.volume:
            try:
                output = system.getoutput('hdiutil', 'unmount', self.volume)
            except system.ExitError:
                print("WARNING: Could not unmount '%s' for '%s'"
                    % (self.volume, self.filename))


class MultiContext(object):
    '''
    This context manager allows you to enter new context managers
    which will all exit when this one exits.
    '''

    def __init__(self):
        super(MultiContext, self).__init__()

    def enter(self, context_manager):
        result = context_manager.__enter__()
        self.children.append(context_manager)
        return result

    def __enter__(self):
        self.children = []
        return self

    def __exit__(self, *args):
        try:
            for child in self.children:
                child.__exit__(*args)
        finally:
            del self.children


def dir_has_contents(directory):
    '''
    Returns True if files that do not start with a period have
    been found in the specified directory, False if not.
    '''

    for filename in os.listdir(directory):
        if not filename.startswith('.'):
            return True
    return False


def select_file(files, key=lambda x: x):
    '''
    Lets the user select a file from a list of filenames. Returns
    the selected file. If the user stops the selection, exits
    the program with the info that the user stopped it.
    '''

    for i, filename in enumerate(files):
        print('  [%d]' % i, os.path.basename(key(filename)))

    while True:
        string = input('> ').strip()
        if not string:
            exit('user stop')

        try:
            selection = int(string)
        except ValueError:
            print("Not a number.", end=' ')
        else:
            if selection < 0 or selection >= len(files):
                print("Invalid selection.", end=' ')
            else:
                break

    return files[selection]


def detect_packages(directory):
    '''
    Finds the paths to the CLTools and Mac OSX SDK packages from
    a directory, or asks the user if they could not be detected.
    Exits if the user exits or if he had no choices.
    '''

    def find_in_files(files, regex):
        for filename in files:
            if re.match(regex, os.path.basename(filename), re.I):
                return filename
        return None

    # Find all *.pkg files, and from this list, match the
    # required files using regular expressions.
    return glob.glob(os.path.join(directory, '*.pkg'))

def unpack_pkg(pkg_filename, dest):
    '''
    Unpacks the contents of a ``*.pkg`` file to the specified
    directory *dest*.
    '''

    system.call('xar', '-C', dest, '-xf', pkg_filename)

def install_pkg(pkg_filename, dest):
    '''
    Installs the contents of a ``*.pkg`` file to the specified folder.
    More specifically, the ``Payload`` file in the package will be
    unzipped into the folder *dest*. A temporary folder needs to be
    created to unpack the *pkg_filename* first.

    .. note:: Sometimes, *pkg_filename* is a directory instead. If that
        is the case, the directory will not be copied into a temporary
        directory.

    :raise RuntimeError: if the Payload file does not exist in the
        ``*.pkg` archive.
    '''

    with MultiContext() as context:
        if os.path.isfile(pkg_filename):
            source_dir = context.enter(TempDir())
            unpack_pkg(pkg_filename, source_dir)
        else:
            source_dir = pkg_filename

        payload_filename = os.path.join(source_dir, 'Payload')
        # If the Payload file does not exist, raise an error.
        if not os.path.isfile(payload_filename):
            raise RuntimeError("'%s' contains no Payload" % pkg_filename)

        # Get the magic characters of the payload to determine
        # whether it's a pbzx file, otherwise use gzip.
        with open(payload_filename, 'rb') as fp:
            magic = fp.read(4)

        commands = []
        if magic == b'pbzx':
            commands.append(['pbzx', '-n', payload_filename])
        else:
            commands.append(['cat', payload_filename])
            commands.append(['gunzip', '-dc'])
        commands.append(['cpio', '-i'])

        # Unpack the contents of the Payload file to the
        # destination directory.
        system.multicall(*commands, cwd=dest)
