# -*- coding: utf-8 -*- #

"""\
ndimake - ndim's minimal implementation of a make-like dependency system
"""

# MIT License
#
# Copyright (c) 2016 Hans Ulrich Niedermann
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from abc import ABCMeta, abstractmethod, abstractproperty

import logging
logger = logging.getLogger(__name__)

import os

import subprocess


def sh(*cmdline):
    """Run an external command without involving the shell"""
    logger.info("Running command: %s", cmdline)
    subprocess.run(cmdline, stdin=subprocess.DEVNULL,
                   shell=False, timeout=120, check=True)


class MakeTarget(metaclass=ABCMeta):

    """Abstract make target"""

    def __init__(self, file_path):
        super(MakeTarget, self).__init__()
        self.__file_path = file_path

    def __str__(self):
        return "%s(%s, %s)" % (self.__class__.__name__,
                               self.file_path,
                               repr(self.dependencies))

    def __repr__(self):
        return self.__str__()

    def ensure_target_dir(self):
        """Make sure the directory of this target exists"""
        dir_path = os.path.dirname(self.file_path)
        if not dir_path:
            pass
        else:
            os.makedirs(dir_path, exist_ok=True)
            if not os.path.isdir(dir_path):
                raise RuntimeError("Directory could not be created: %s" % dir_path)

    @property
    def file_path(self):
        """Path of the file this target represents"""
        return self.__file_path

    def timestamp(self):
        """Timestamp for this target"""
        if os.path.exists(self.file_path):
            return os.stat(self.file_path).st_mtime
        else:
            return 0

    def update(self):
        """Update this target conditionally"""
        if self.dirty():
            self.update_deps()
            self.ensure_target_dir()
            self.do_update()

    def update_deps(self):
        """Make sure all our deps are up to date"""
        for dep in self.dependencies:
            dep.update()

    @abstractproperty
    def dependencies(self):
        """List of this target's dependencies"""
        return []

    @abstractmethod
    def dirty(self):
        """Whether this target needs to be rebuilt"""
        return True

    @abstractmethod
    def do_update(self):
        """Unconditionally run the actual update actions"""
        pass


class SourceFile(MakeTarget):

    """Represent a source file without dependencies"""

    @property
    def dependencies(self):
        """A source file by definition has no dependencies"""
        return []

    def dirty(self):
        """We CANNOT be dirty - but the file MUST exist"""
        if os.path.exists(self.file_path):
            return False
        else:
            raise RuntimeError("Source file missing: %s" % self.file_path)

    def do_update(self):
        """There are no update actions to run - but the file MUST exist"""
        if os.path.exists(self.file_path):
            pass
        else:
            raise RuntimeError("Source file missing: %s" % self.file_path)


class FileConverter(MakeTarget):

    """This target file depends on some other files"""

    def dirty(self):
        """Whether we need to rebuild this"""
        if not os.path.exists(self.file_path):
            return True
        for dep in self.dependencies:
            if dep.dirty():
                return True
            if dep.timestamp() > self.timestamp():
                return True
        return False


class Hardlink(FileConverter):

    """Hard link the dependency to this file"""

    def __init__(self, file_path, src):
        super(Hardlink, self).__init__(file_path)
        self.src = src

    @property
    def dependencies(self):
        return [ self.src ]

    def do_update(self):
        if os.path.exists(self.file_path):
            os.unlink(self.file_path)
        os.link(self.src.file_path, self.file_path, follow_symlinks=False)


class VirtualTarget(FileConverter):

    """non-file target which just remakes all its dependencies

    Similar to make's `.PHONY: foo` targets.
    """

    def __init__(self, deps):
        """Choose some unique string as file_path"""
        super(VirtualTarget, self).__init__("virtual-target-%x" % hash(self))
        self.__deps = deps

    @property
    def dependencies(self):
        return self.__deps

    def do_update(self):
        pass
