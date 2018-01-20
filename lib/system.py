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

import os
import pipes
import six
import subprocess
import sys

#: True if verbose output is desired.
verbose = True


class ExitError(Exception):

    def __init__(self, args, code):
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
        'stdin': kwargs.pop('stdin', None if verbose else subprocess.DEVNULL),
        'stdout': kwargs.pop('stdout', None if verbose else subprocess.DEVNULL),
        'stderr': kwargs.pop('stderr', None if verbose else subprocess.DEVNULL),
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
