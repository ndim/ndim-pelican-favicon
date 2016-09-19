# -*- coding: utf-8 -*- #

from pelican import signals

from . import favicon

def register():
    signals.get_generators.connect(favicon.sig_get_generators)
