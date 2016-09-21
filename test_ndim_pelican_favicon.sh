#!/bin/sh
#
# My local test launching helper script

set -e
cd "$(dirname "$0")"

env PYTHONPATH="$HOME/.local/lib/python3.5/site-packages:$PWD/../pelican:$PWD/.." \
    python3 -m ndim_pelican_favicon.test_ndim_pelican_favicon
