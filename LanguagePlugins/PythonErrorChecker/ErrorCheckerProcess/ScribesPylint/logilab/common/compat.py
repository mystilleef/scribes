# pylint: disable=E0601,W0622,W0611
# copyright 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-common.
#
# logilab-common is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option) any
# later version.
#
# logilab-common is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with logilab-common.  If not, see <http://www.gnu.org/licenses/>.
"""Wrappers around some builtins introduced in python 2.3, 2.4 and
2.5, making them available in for earlier versions of python.

See another compatibility snippets from other projects:
    
    :mod:`lib2to3.fixes`
    :mod:`coverage.backward`
    :mod:`unittest2.compatibility`
"""

from __future__ import generators

__docformat__ = "restructuredtext en"

import os
import sys
from warnings import warn

import __builtin__ as builtins # 2to3 will tranform '__builtin__' to 'builtins'

if sys.version_info < (3, 0):
    str_to_bytes = str
    def str_encode(string, encoding):
        if isinstance(string, unicode):
            return string.encode(encoding)
        return str(string)
else:
    def str_to_bytes(string):
        return str.encode(string)
    # we have to ignore the encoding in py3k to be able to write a string into a
    # TextIOWrapper or like object (which expect an unicode string)
    def str_encode(string, encoding):
        return str(string)

# XXX shouldn't we remove this and just let 2to3 do his job ?
try:
    callable = callable
except NameError:# callable removed from py3k
    import collections
    def callable(something):
        return isinstance(something, collections.Callable)
    del collections

if sys.version_info < (3, 0):
    raw_input = raw_input
else:
    raw_input = input

# Pythons 2 and 3 differ on where to get StringIO
if sys.version_info < (3, 0):
    from cStringIO import StringIO
    FileIO = file
    BytesIO = StringIO
else:
    from io import FileIO, BytesIO, StringIO

# Where do pickles come from?
try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    set = set
    frozenset = frozenset
except NameError:# Python 2.3 doesn't have `set`
    from sets import Set as set, ImmutableSet as frozenset

from logilab.common.deprecation import deprecated

from itertools import izip, chain, imap
izip = deprecated('izip exists in itertools since py2.3')(izip)
imap = deprecated('imap exists in itertools since py2.3')(imap)
chain = deprecated('chain exists in itertools since py2.3')(chain)

sum = deprecated('sum exists in builtins since py2.3')(sum)
enumerate = deprecated('enumerate exists in builtins since py2.3')(enumerate)

try:
    sorted = sorted
    reversed = reversed
except NameError: # py2.3

    def sorted(iterable, cmp=None, key=None, reverse=False):
        original = list(iterable)
        if key:
            l2 = [(key(elt), index) for index, elt in builtins.enumerate(original)]
        else:
            l2 = original
        l2.sort(cmp)
        if reverse:
            l2.reverse()
        if key:
            return [original[index] for elt, index in l2]
        return l2

    def reversed(l):
        l2 = list(l)
        l2.reverse()
        return l2

try:
    max = max
    max(("ab","cde"),key=len) # does not work in py2.3
except TypeError:
    def max( *args, **kargs):
        if len(args) == 0:
            raise TypeError("max expected at least 1 arguments, got 0")
        key= kargs.pop("key", None)
        #default implementation
        if key is None:
            return builtins.max(*args,**kargs)

        for karg in kargs:
            raise TypeError("unexpected keyword argument %s for function max") % karg

        if len(args) == 1:
            items = iter(args[0])
        else:
            items = iter(args)

        try:
            best_item = items.next()
            best_value = key(best_item)
        except StopIteration:
            raise ValueError("max() arg is an empty sequence")

        for item in items:
            value = key(item)
            if value > best_value:
                best_item = item
                best_value = value

        return best_item


# Python2.5 builtins
try:
    any = any
    all = all
except NameError:
    def any(iterable):
        """any(iterable) -> bool

        Return True if bool(x) is True for any x in the iterable.
        """
        for elt in iterable:
            if elt:
                return True
        return False

    def all(iterable):
        """all(iterable) -> bool

        Return True if bool(x) is True for all values x in the iterable.
        """
        for elt in iterable:
            if not elt:
                return False
        return True


# Python2.5 subprocess added functions and exceptions
try:
    from subprocess import Popen
except ImportError:
    # gae or python < 2.3

    class CalledProcessError(Exception):
        """This exception is raised when a process run by check_call() returns
        a non-zero exit status.  The exit status will be stored in the
        returncode attribute."""
        def __init__(self, returncode, cmd):
            self.returncode = returncode
            self.cmd = cmd
        def __str__(self):
            return "Command '%s' returned non-zero exit status %d" % (self.cmd,
    self.returncode)

    def call(*popenargs, **kwargs):
        """Run command with arguments.  Wait for command to complete, then
        return the returncode attribute.

        The arguments are the same as for the Popen constructor.  Example:

        retcode = call(["ls", "-l"])
        """
        # workaround: subprocess.Popen(cmd, stdout=sys.stdout) fails
        # see http://bugs.python.org/issue1531862
        if "stdout" in kwargs:
            fileno = kwargs.get("stdout").fileno()
            del kwargs['stdout']
            return Popen(stdout=os.dup(fileno), *popenargs, **kwargs).wait()
        return Popen(*popenargs, **kwargs).wait()

    def check_call(*popenargs, **kwargs):
        """Run command with arguments.  Wait for command to complete.  If
        the exit code was zero then return, otherwise raise
        CalledProcessError.  The CalledProcessError object will have the
        return code in the returncode attribute.

        The arguments are the same as for the Popen constructor.  Example:

        check_call(["ls", "-l"])
        """
        retcode = call(*popenargs, **kwargs)
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        if retcode:
            raise CalledProcessError(retcode, cmd)
        return retcode

try:
    from os.path import relpath
except ImportError: # python < 2.6
    from os.path import curdir, abspath, sep, commonprefix, pardir, join
    def relpath(path, start=curdir):
        """Return a relative version of a path"""

        if not path:
            raise ValueError("no path specified")

        start_list = abspath(start).split(sep)
        path_list = abspath(path).split(sep)

        # Work out how much of the filepath is shared by start and path.
        i = len(commonprefix([start_list, path_list]))

        rel_list = [pardir] * (len(start_list)-i) + path_list[i:]
        if not rel_list:
            return curdir
        return join(*rel_list)

if (2, 5) <= sys.version_info[:2]:
    InheritableSet = set
else:
    class InheritableSet(set):
        """hacked resolving inheritancy issue from old style class in 2.4"""
        def __new__(cls, *args, **kwargs):
            if args:
                new_args = (args[0], )
            else:
                new_args = ()
            obj = set.__new__(cls, *new_args)
            obj.__init__(*args, **kwargs)
            return obj

# XXX shouldn't we remove this and just let 2to3 do his job ?
# range or xrange?
try:
    range = xrange
except NameError:
    range = range

# ConfigParser was renamed to the more-standard configparser
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        json = None
