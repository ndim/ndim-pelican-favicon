# -*- coding: utf-8 -*- #

"""\
favicon - pelican plugin to convert SVG favicon into a number of bitmap files
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


from pelican.generators import Generator


from abc import ABCMeta, abstractmethod, abstractproperty


import logging
logger = logging.getLogger(__name__)

import os


from PIL import Image


from . import ndimake


class SVG2PNG(ndimake.FileConverter):

    """Convert an SVG image to an PNG image"""

    def __init__(self, file_path, svg_file, sz):
        super(SVG2PNG, self).__init__(file_path)
        self.svg_file = svg_file
        self.sz = sz

    @property
    def dependencies(self):
        return [ self.svg_file ]

    def dirty(self):
        if super(SVG2PNG, self).dirty():
            return True

        # Check whether this rule would generate the same image
        # format and dimensions as the existing image file has.
        im = Image.open(self.file_path)
        if (self.sz, self.sz) != im.size:
            logger.debug("existing file %s has im.size %s (should be %s)",
                         self.file_path, im.size, (self.sz, self.sz))
            return True
        if im.format != 'PNG':
            logger.debug("existing file %s has im.format %s (should be %s)",
                         self.file_path, im.format, 'PNG')
            return True

        return False

    def do_update(self):
        # We could try to do this without running external programs
        # and probably be quicker, but we know inkscape works well so
        # we start with an implementation known to work and maybe
        # change the implementation later.
        ndimake.sh('inkscape',
                   '--without-gui',
                   '--export-area-drawing',
                   '--export-png=%s' % self.file_path,
                   '--export-width=%d' % self.sz,
                   self.svg_file.file_path)
        ndimake.sh('pngcrush',
                   '-q',
                   '-ow',
                   self.file_path)


class ICOTarget(ndimake.FileConverter):

    """Generate ICO file from a number of PNG bitmaps"""

    def __init__(self, file_path, png_sources):
        super(ICOTarget, self).__init__(file_path)
        self.png_sources = png_sources

    @property
    def dependencies(self):
        return self.png_sources

    def do_update(self):
        cmdline = ['icotool',
                   '--create',
                   '--output=%s' % self.file_path,
        ] + [ src.file_path for src in self.png_sources ]
        ndimake.sh(*cmdline)


class FaviconGenerator(Generator):

    """Pelican Generator generating favicon bitmap files from SVG favicon"""

    def __init__(self, *args, **kwargs):
        # We do not care about the constructor arguments, we just need
        # to pass them on.
        super(FaviconGenerator, self).__init__(*args, **kwargs)

        # Retrieve settings
        self.favicon_svg_source_fpath = self.settings.get('FAVICON_SVG_SOURCE',
                                                          'favicon.svg')
        self.favicon_output_path = self.settings.get('FAVICON_OUTPUT_PATH',
                                                     'favicon')
        self.favicon_double_res = self.settings.get('FAVICON_DOUBLE_RES', True)

        svg_srcfile  = ndimake.SourceFile(os.path.join(self.path,
                                                       self.favicon_svg_source_fpath))

        def tjoin(fname):
            return os.path.join(self.output_path, self.favicon_output_path, fname)

        # Compose list of targets
        targets = []

        ico_sizes = [16, 32, 48]
        ico_png_list = [ SVG2PNG(tjoin('favicon-%dx%d.png' % (sz, sz)),
                                 svg_srcfile, sz)
                         for sz in ico_sizes ]
        targets.append(ICOTarget(os.path.join(self.output_path, 'favicon.ico'),
                                 ico_png_list))

        targets.append(SVG2PNG(tjoin('favicon.png'), svg_srcfile, 196))
        targets.append(SVG2PNG(tjoin('apple-touch-icon.png'), svg_srcfile, 180))

        if self.favicon_double_res:
            targets.append(SVG2PNG(tjoin('favicon@2x.png'), svg_srcfile, 392))
            targets.append(SVG2PNG(tjoin('apple-touch-icon@2x.png'), svg_srcfile, 360))

        self.target = ndimake.VirtualTarget(targets)

    def __str__(self):
        fmt = ("%s("
               "FAVICON_SVG_SOURCE=%s,"
               "FAVICON_OUTPUT_PATH=%s,"
               "FAVICON_DOUBLE_RES=%s,"
               "path=%s,"
               "output_path=%s"
               ")")
        return fmt % (self.__class__.__name__,
                      repr(self.favicon_svg_source_fpath),
                      repr(self.favicon_output_path),
                      repr(self.favicon_double_res),
                      repr(self.path),
                      repr(self.output_path))

    def generate_context(self):
        """Pelican plugin interface method"""
        logger.debug("%s generate_context", self.__class__.__name__)

    def generate_output(self, writer=None):
        """Pelican plugin interface method"""
        logger.debug("%s generate_output %s",
                     self.__class__.__name__, writer)
        self.target.update()


def sig_get_generators(generators):
    """Signal handler to be registered with Pelican"""
    return FaviconGenerator
