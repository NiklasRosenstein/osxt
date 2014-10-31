#!/usr/bin/env python
#
# Create a local installation of the Mac OS Command Line Tools.
# Copyright (C) 2014 Niklas Rosenstein
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

import sys, os
import re, glob, pipes, shutil, tempfile, argparse, subprocess

DIRNAME = os.path.dirname(__file__)

parser = argparse.ArgumentParser(description='''
    Create a local installation of the Mac OS Command Line Tools from
    a Disk Image File. For installation that includes the Mac OS SDK
    components, must be run as superuser.''')
parser.add_argument('dmg', help='''
    The Disk Image File that contains the Mac OS Command Line Tools.''')
parser.add_argument('dest', help='''
    The destination folder which will contain all the files that would
    normally be installed into your root directory.''')
parser.add_argument('-o', '--owner', help='''
    The name of the new owner of the output directory and all its
    contents. This option should be specified when running as superuser
    as it can not figure out the original user name.''')
parser.add_argument('--no-sdk', action='store_true', help='''
    If specified, the Mac OS SDK will not be extracted from the Disk
    Image File.''')
parser.add_argument('--no-cltools', action='store_true', help='''
    If specified, the Command Line Tools will not be extracted from
    the Disk Image File.''')
parser.add_argument('-q', '--quiet', action='store_true', help='''
    Be very quiet. Passing this option will disable the output of
    the commands that have been run and hide the command arguments.''')

singleton = lambda x: x()

@singleton
class System:
    '''
    This is a utility namespace for performing system calls.
    '''

    class ExitError(Exception):
        pass

    verbose = True

    def format(self, *args):
        return ' '.join(pipes.quote(x) for x in args)

    def call(self, *args):
        if self.verbose:
            print('$', self.format(*args))
            stdout = stderr = 1
        else:
            stdout = subprocess.PIPE
            stderr = subprocess.STDOUT
        process = subprocess.Popen(args, shell=False)
        process.wait()
        if process.returncode != 0:
            raise self.ExitError(args, process.returncode)

    def getoutput(self, *args):
        if self.verbose:
            print('$', self.format(*args))
        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        stdout = process.communicate()[0]
        if process.returncode != 0:
            raise self.ExitError(args, process.returncode)
        return stdout

    def multicall(self, *commands, **kwargs):
        '''
        :param stdin: The standard input of the first command. Defaults
            to None (no input).
        :param stdout: The output descriptor for the last command in
            the multicall. Defaults to None (the current standard output).
            If this is `subprocess.PIPE`, this method will return the
            output of the last process.
        :param stderr: The output descriptor for the last commands in
            the multicall. Defaults to None (the current standard error
            output).
        :param cwd: The current working directory for all commands.
            Defaults to None (the current working directory is used).
        '''

        # Read additional options for the call.
        data = {
            'stdin': kwargs.pop('stdin', None),
            'stdout': kwargs.pop('stdout', None),
            'stderr': kwargs.pop('stderr', None),
            'cwd': kwargs.pop('cwd', None),
        }

        # Issue any remaining, not handled keyword arguments.
        for key in kwargs:
            raise TypeError("unexpected keyword argument '%s'" % key)

        # There must be at least one command specified to be executed.
        if not commands:
            raise TypeError("'*commands' must not be empty")
        for command in commands:
            if not isinstance(command, (list, tuple)):
                raise TypeError("'*command' item must be list/tuple, got %s"
                    % type(command).__name__)

        # Print an approximate shell representation of the call.
        if self.verbose:
            print('$', ' | '.join(self.format(*c) for c in commands))

        # Spawn the processes, handling the first and last special.
        processes = []
        for index, command in enumerate(commands):

            # Determine the stdin, stdout and stderr for this process.
            if index == 0:
                stdin = data['stdin']
                stdout = subprocess.PIPE
                stderr = None
            else:
                stdin = processes[-1].stdout
            if index == (len(commands) - 1):
                stdout = data['stdout']
                stderr = data['stderr']

            # Create a new process and append it to the processes list.
            process = subprocess.Popen(command, stdin=stdin, stdout=stdout,
                stderr=stderr, cwd=data['cwd'])
            processes.append(process)

        # Wait until all processes are finished.
        for process in processes:
            process.wait()

        # If the last process exited with a non-zero returncode,
        # raise an appropriate exception.
        if processes[-1].returncode != 0:
            raise self.ExitError(commands[-1], processes[-1].returncode)

        if data['stdout'] == subprocess.PIPE:
            return processes.communicate()[0]

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

    def __init__(self, filename):
        super(MountFile, self).__init__()
        self.filename = filename
        self.volume = None

    def __enter__(self):
        # Run the hdiutil command to mount the file and determine
        # the Volume at which it was mounted.
        try:
            output = System.getoutput('hdiutil', 'mount', self.filename)
        except System.ExitError:
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
                output = System.getoutput('hdiutil', 'unmount', self.volume)
            except System.ExitError:
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

def chown_recurse(path, uid, gid):
    '''
    Changes the ownership of a complete directory tree to the
    specified user and group id. Does not follow symbolic links.
    '''

    isdir = os.path.isdir(path)
    if isdir or os.path.isfile(path):
        os.chown(path, uid, gid)

    if isdir:
        for name in os.listdir(path):
            full = os.path.join(path, name)
            chown_recurse(full, uid, gid)

def select_file(files):
    '''
    Lets the user select a file from a list of filenames. Returns
    the selected file. If the user stops the selection, exits
    the program with the info that the user stopped it.
    '''

    for i, filename in enumerate(files):
        print('[%d]' % i, os.path.basename(filename))

    while True:
        string = raw_input('Please choose (empty to quit): ').strip()
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

def detect_packages(directory, options):
    '''
    Finds the paths to the CLTools and Mac OSX SDK packages from
    a directory, or asks the user if they could not be detected.
    Exits if the user exits or if he had no choices.

    The returned dictionary contains the filenames to the packages
    that have been found. Note that if a package was not found and
    it should not be installed per the specified options, the path
    to the package may be none as the user is not asked for it.
    '''

    def find_in_files(files, regex):
        for filename in files:
            if re.match(regex, os.path.basename(filename), re.I):
                return filename
        return None

    # Find all *.pkg files, and from this list, match the
    # required files using regular expressions.
    pkgs = glob.glob(os.path.join(directory, '*.pkg'))
    cltools_pkg = find_in_files(pkgs, 'cltools.*')
    sdk_pkg = find_in_files(pkgs, '.*sdk.*')

    # If either of them could not be found, ask the user.
    if not cltools_pkg and not options.no_cltools:
        print('The CLTools Package could not be found.')
        cltools_pkg = select_file(pkgs)
    if not sdk_pkg and not options.no_sdk:
        print('The Mac OSX SDK package could not be found.')
        sdk_pkg = select_file(pkgs)

    return {'cltools': cltools_pkg, 'sdk': sdk_pkg}

def unpack_pkg(pkg_filename, dest):
    '''
    Unpacks the contents of a ``*.pkg`` file to the specified
    directory *dest*.
    '''

    System.call('xar', '-C', dest, '-xf', pkg_filename)

def install_pkg(pkg_filename, dest):
    '''
    Installs the contents of a ``*.pkg`` file to the specified folder.
    More specifically, the ``Payload`` file in the package will be
    unzipped into the folder *dest*. A temporary folder needs to be
    created to unpack the *pkg_filename* first.

    :raise RuntimeError: if the Payload file does not exist in the
        ``*.pkg` archive.
    '''

    with TempDir() as tmpdir:
        # Unpack the PKG archive and get the path to the Payload file.
        unpack_pkg(pkg_filename, tmpdir)
        payload_filename = os.path.join(tmpdir, 'Payload')

        # If the Payload file does not exist, raise an error.
        if not os.path.isfile(payload_filename):
            raise RuntimeError("'%s' contains no Payload" % pkg_filename)

        # Unpack the contents of the Payload file to the
        # destination directory.
        System.multicall(
            ['cat', payload_filename],
            ['gunzip', '-dc'],
            ['cpio', '-i'],
            cwd=dest)

def main():
    # Parse the command-line arguments.
    args = parser.parse_args()
    if args.quiet:
        System.verbose = False

    # If the Mac OS SDK should be installed, this should be run
    # as superuser. Otherwise, some files might not be extracted
    # properly from the archive.
    if not args.no_sdk and os.getuid() != 0:
        exit('run as superuser if you want to install the SDK')

    # Determine the user and group ID of the new owner.
    if args.owner:
        try:
            uid = int(System.getoutput('id', '-u', args.owner))
            gid = int(System.getoutput('id', '-g', args.owner))
        except (ValueError, System.ExitError):
            exit('could not determine uid/gid for user', args.owner)
    else:
        uid = gid = None

    # Make sure the output directory exists, and that it does
    # not already contain any important files.
    if os.path.exists(args.dest):
        if not os.path.isdir(args.dest):
            exit("'%s' is not a directory" % args.dest)

        if dir_has_contents(args.dest):
            string = raw_input("'%s' is not empty, it'll be erased. "
                "Okay with that? [yes/no] " % args.dest).strip().lower()
            if not string or string not in ('yes', 'y'):
                exit('user stop')

            System.call('rm', '-r', args.dest)
            System.call('mkdir', args.dest)
    else:
        System.call('mkdir', '-p', args.dest)

    # Mount the Disk Image File and search for the CLTools and
    # Mac OS SDK package files.
    packages = None
    with MultiContext() as context:
        volume = context.enter(MountFile(args.dmg))

        # Two choices: Either, the CLTools and SDK packages are
        # contained in a Packages/ subdirectory or in another
        # Package archive.
        packages_dir = os.path.join(volume, 'Packages')
        if os.path.isdir(packages_dir):
            packages = detect_packages(packages_dir, args)
        else:
            # So, there must be a *.pkg file in this Disk Image File
            # which in turn contains the CLTools and SDK packages.
            pkgs = glob.glob(os.path.join(volume, '*.pkg'))
            if not pkgs:
                exit('No *.pkg found in Disk Image File', code=1)
            elif len(pkgs) != 1:
                print('Not sure which *.pkg to use from Disk Image File.')
                filename = select_file(pkgs)
            else:
                filename = pkgs[0]

            # We need to unpack the PKG in order to acces its
            # contained packages (the CLTools and SDK packages).
            tmpdir = context.enter(TempDir())
            unpack_pkg(filename, tmpdir)
            packages = detect_packages(tmpdir, args)

        # Now that we have detected the packages which are to
        # be installed, we can safely install them to the output
        # folder.
        if not args.no_sdk:
            install_pkg(packages['sdk'], args.dest)
        if not args.no_cltools:
            install_pkg(packages['cltools'], args.dest)

    # Copy the activate script to the destination directory.
    activate_script = os.path.join(DIRNAME, 'scripts', 'activate')
    try:
        System.call('cp', activate_script, os.path.join(args.dest, 'activate'))
    except System.ExitError as exc:
        print("failed to copy activate script.")

    # Chown the complete destination directory.
    if args.owner:
        chown_recurse(args.dest, uid, gid)

    return 0

def exit(*message, **kwargs):
    code = kwargs.get('code', 0)
    for key in kwargs:
        raise TypeError("unexpected keyword argument '%s'" % key)
    print(sys.argv[0], '***', *message, file=sys.stderr)
    sys.exit(code)

if __name__ == "__main__":
    sys.exit(main())

