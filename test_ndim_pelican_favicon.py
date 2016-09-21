# -*- coding: utf-8 -*- #

"""\
test the ndim_pelican_favicon plugin
"""

import os
from pprint import pprint

from pelican.tests.support import unittest, get_settings
from . import favicon

file_path = os.path.dirname(__file__)
test_data_path = os.path.join(file_path, 'test_data')


class FaviconTest(unittest.TestCase):

    def check_files(self, path, fav_path):
        fl = [ 'favicon.ico',
              os.path.join(fav_path, 'apple-touch-icon.png'),
              os.path.join(fav_path, 'apple-touch-icon@2x.png'),
              os.path.join(fav_path, 'favicon.png'),
              os.path.join(fav_path, 'favicon@2x.png'),
              os.path.join(fav_path, 'favicon-16x16.png'),
              os.path.join(fav_path, 'favicon-32x32.png'),
              os.path.join(fav_path, 'favicon-48x48.png'),
        ]
        for fn in fl:
            s = os.stat(os.path.join(path,fn))

    def test_foo(self):
        settings = get_settings()
        fav_path = 'favicon'
        # settings['FAVICON_OUTPUT_PATH'] = fav_path
        # pprint(settings)
        op = os.path.join('__test_output', 'bar')
        generator = favicon.FaviconGenerator(context=settings.copy(),
                                             settings=settings,
                                             path=test_data_path,
                                             theme=settings['THEME'],
                                             output_path=op)
        # print("generator", generator)
        # pprint(dir(generator))
        generator.generate_context()
        generator.generate_output(writer=None)
        self.check_files(op, fav_path)

    def test_bar(self):
        settings = get_settings().copy()
        fav_path = 'images'
        settings['FAVICON_OUTPUT_PATH'] = fav_path
        # pprint(settings)
        op = os.path.join('__test_output', 'bar')
        generator = favicon.FaviconGenerator(context=settings,
                                             settings=settings,
                                             path=test_data_path,
                                             theme=settings['THEME'],
                                             output_path=op)
        # print("generator", generator)
        # pprint(dir(generator))
        generator.generate_context()
        generator.generate_output(writer=None)
        self.check_files(op, fav_path)


if __name__ == '__main__':
    unittest.main()
