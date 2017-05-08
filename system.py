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

import os
import pipes
import six
import subprocess
import sys

#: True if verbose output is desired.
verbose = True

class ExitError(Exception):

    def __init__(args, code):
        self.args = args
        self.code = code

    def __str__(self):
        return '{}: {}'.format(self.args[0], self.code)


def dec(value, encoding=sys.getdefaultencoding()):
  if not isinstance(value, six.text_type):
    return value.decode(encoding)
  return value


def format(*args):
    return ' '.join(pipes.quote(x) for x in args)


def call(*args):
    if verbose:
        print('$', format(*args))
        stdout = stderr = 1
    else:
        stdout = subprocess.PIPE
        stderr = subprocess.STDOUT
    process = subprocess.Popen(args, shell=False)
    process.wait()
    if process.returncode != 0:
        raise ExitError(args, process.returncode)


def getoutput(*args):
    if verbose:
        print('$', format(*args))
    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    stdout = process.communicate()[0]
    if process.returncode != 0:
        raise ExitError(args, process.returncode)
    return dec(stdout)


def multicall(*commands, **kwargs):
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
    if verbose:
        if data['cwd']:
            print('$ cd', os.path.abspath(data['cwd']))
        print('$', ' | '.join(format(*c) for c in commands))

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
        raise ExitError(commands[-1], processes[-1].returncode)

    if data['stdout'] == subprocess.PIPE:
        return processes.communicate()[0]
