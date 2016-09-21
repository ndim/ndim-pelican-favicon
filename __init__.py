# -*- coding: utf-8 -*- #

"""\
ndim_pelican_favicon top level package
"""

from pelican import signals

from . import favicon

def register():
    """Register ndim_pelican_favicon with Pelican"""
    signals.get_generators.connect(favicon.sig_get_generators)
