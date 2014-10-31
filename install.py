#!/usr/bin/env python
#
# Non-global installation for Mac OS Command Line Tools.
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
import re, glob, pipes, shutil, argparse, subprocess, tempfile

cwd = os.getcwd()

parser = argparse.ArgumentParser(description='''
    Install Mac OS Command Line Tools to a specific directory. Note that
    you should run this command as superuser, otherwise there will be
    trouble unpacking the Mac OS SDK from the archive.''')
parser.add_argument('archive', help='''The archive that contains the Command
    Line Tools which must be a *.dmg file.''')
parser.add_argument('dest', help='''The destination output folder. The
    Command Line Tools will be installed to this folder and a script
    to activate the tools will be put there as well.''')
parser.add_argument('-o', '--owner', help='''
    The new owner of the expanded files. Since you need to call this
    script as superuser, the it can not determine by itself what user
    you are.''')
parser.add_argument('-f', '--force', help='''Force overwrite if the
    directory already exists. Otherwise, you will be prompted in the
    console.''')

class ExitError(Exception):
    pass

def call(*args):
    print('$', ' '.join(pipes.quote(x) for x in args))
    process = subprocess.Popen(args)
    process.wait()
    if process.returncode != 0:
        raise ExitError(args, process.returncode)

def callget(*args):
    print('$', ' '.join(pipes.quote(x) for x in args))
    process = subprocess.Popen(args, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    stdout = process.communicate()[0]
    if process.returncode != 0:
        raise ExitError(args, process.returncode)
    return stdout.strip()

def pipecall(*commands, **kwargs):
    join = kwargs.pop('joinerr', False)
    stdin = kwargs.pop('stdin', None)
    stdout = kwargs.pop('stdout', subprocess.PIPE)
    stderr = kwargs.pop('stderr', subprocess.STDOUT if join else None)
    cwd = kwargs.pop('cwd', None)
    for key in kwargs:
        raise TypeError('unexpected keyword argument "%s"' % key)

    if not commands:
        raise TypeError('expected at least one command')

    print('$', ' | '.join(' '.join(pipes.quote(x) for x in c) for c in commands))

    processes = []
    for index, command in enumerate(commands):
        if processes:
            stdin = processes[-1].stdout
            if index == (len(commands) - 1):
                stdout = None
            else:
                stdout = subprocess.PIPE
            stderr = subprocess.STDOUT if join else None
        process = subprocess.Popen(command, stdin=stdin, stdout=stdout,
            stderr=stderr, cwd=cwd)
        processes.append(process)

    for process in processes:
        process.wait()
    if processes and processes[-1].returncode != 0:
        raise ExitError(commands[-1], processes[-1].returncode)

class MountFile(object):
    '''
    Uses hdiutil to mount and unmount a file and returns the
    volume name at which it was mounted.
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
            output = callget('hdiutil', 'mount', self.filename)
        except ExitError:
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
                output = callget('hdiutil', 'unmount', self.volume)
            except ExitError:
                print("WARNING: Could not unmount '%s' for '%s'"
                    % (self.volume, self.filename))

def exit(*args):
    '''
    Exits the script with returncode 1 after printing the
    message in *\*args*.
    '''

    print(sys.argv[0], '***', *args)
    sys.exit(1)

def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
    elif not os.path.isdir(path):
        raise OSError('"%s" is not a directory' % path)

def find_in_filelist(files, regex, ignore_case=True):
    flags = 0
    if ignore_case:
        flags = re.I
    expr = re.compile(regex, flags)
    for filename in files:
        if expr.match(filename):
            return filename
    return None

def chown(path, uid, gid):
    os.chown(path, uid, gid)
    if os.path.isdir(path):
        for name in os.listdir(path):
            full = os.path.join(path, name)
            if os.path.isdir(full) or os.path.isfile(full):
                chown(full, uid, gid)

def extract_pkg_payload(pkg, folder):
    tempdir = tempfile.mkdtemp()
    try:
        call('xar', '-C', tempdir, '-xf', pkg)
        payload = os.path.join(tempdir, 'Payload')
        if not os.path.isfile(payload):
            print('error: "%s" does not contain a Payload file' % pkg)
            # todo: What to do now?
            return

        # Extract the contents of the Payload file to the
        # destination directory.
        pipecall(['cat', payload], ['gunzip', '-dc'], ['cpio', '-i'], cwd=folder)
    finally:
        shutil.rmtree(tempdir)

def main():
    args = parser.parse_args()

    # Must be called as superuser.
    if os.getuid() != 0:
        exit('Please run as superuser, otherwise files can not be extracted properly.')

    # Determine the User and Group ID for the extracted archives.
    if args.owner:
        try:
            uid = int(callget('id', '-u', args.owner))
            gid = int(callget('id', '-g', args.owner))
        except (ExitError, ValueError):
            exit("could not determine uid/gid for user", args.owner)
    else:
        uid, gid = os.getuid(), os.getgid()
        args.owner = 'root'

    # Make sure the destination directory is not empty.
    if os.path.exists(args.dest) and not os.path.isdir(args.dest):
        exit('"%s" is not a directory.' % args.dest)
    elif os.path.isdir(args.dest):
        if not args.force:
            print('"%s" already exists.' % args.dest)
            result = raw_input('Do you want to loose all its existing files? [Yes/no] ')
            if result.lower().strip() != 'yes':
                return 0

        call('rm', '-rf', args.dest)

    # Make sure the archive exists and has the right suffix.
    if not os.path.exists(args.archive):
        exit('"%s" is not a file' % args.dest)
    elif not os.path.isfile(args.archive):
        exit('"%s" does not exist' % args.dest)
    elif not args.archive.endswith('.dmg'):
        exit('not a *.dmg archive')

    makedirs(args.dest)

    # Mount the archive.
    with MountFile(args.archive) as volume:
        # Find the *.pkg files in the Packages/ directory of
        # the mounted archive.
        files = glob.glob(os.path.join(volume, 'Packages', '*.pkg'))

        # Determine which PKG contains the CL Tools and which
        # contains the SDK.
        cltools = find_in_filelist(files, '.*CLTools.*')
        sdk = find_in_filelist(files, '.*MacOSX.*SDK.*')

        if not cltools or not sdk:
            exit('Archive contains no CLTools (n)or MacOSX SDK')

        extract_pkg_payload(cltools, args.dest)
        extract_pkg_payload(sdk, args.dest)

    # Own the complete folder.
    print("changing owner of extracted files to", args.owner)
    chown(args.dest, uid, gid)

    # Copy the activation script to the destination directory.
    script = os.path.join(os.path.dirname(__file__), 'scripts', 'activate')
    if os.path.isfile(script):
        call('cp', script, os.path.join(args.dest, 'activate'))
    else:
        print('Warning: activate script could not be copied')

    return 0

if __name__ == "__main__":
    sys.exit(main())

