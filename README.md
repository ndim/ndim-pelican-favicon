ndim_pelican_favicon
====================

`ndim_pelican_favicon` is a [pelican](http://getpelican.com/) plugin
which takes an original SVG file containing a favicon type graphic and
generates a `favicon.ico` file and an assortment of PNG files.

These bitmap files can then be used in the Pelican theme's definition
of the HTML `<head>` element for proper integration into browser
bookmarks, smartphone touch icons, etc.

You can find the `ndim_pelican_favicon` source code on
[ndim's `ndim_pelican_favicon` repository page on github](https://github.com/ndim/ndim_pelican_favicon).


Requirements
------------

`ndim_pelican_favicon` runs the external tools
[`inkscape`](http://inkscape.sourceforge.net/),
[`pngcrush`](http://pmt.sourceforge.net/pngcrush/), and
[`icotool`](http://www.nongnu.org/icoutils/) which must be installed
independently.

`ndim_pelican_favicon` has been developed and tested on a on Fedora 24
Linux systems with Python 3.5 using Pelican 3.6.3 and the
`pelican-bootstrp3` theme.


Configuration
-------------

`ndim_pelican_favicon` defines a few new Pelican settings:

  * `FAVICON_SVG_SOURCE` (default: `'favicon.svg'`)

    Location of the source SVG file with the favicon,
    relative to `PATH`.

  * `FAVICON_OUTPUT_PATH` (default: `'favicon'`)

    Path to put the generated images to, relative to `OUTPUT_PATH`.

    The one exception is the favicon.ico file which is by convention
    looked for and thus stored in `OUTPUT_PATH` directly.

  * `FAVICON_DOUBLE_RES` (default: `True`)

    For every PNG file `foo.png`, generate a file `foo@2x.png` with
    twice the resolution.

The following stock Pelican settings are also used by
`ndim_pelican_favicon`:

  * `PATH`

    Location of the source files.

  * `OUTPUT_PATH`

    Location of the output files.

There are other Pelican settings which need to be set properly to work
together with the `FAVICON_*` settings, and you have to set them
manually in `pelicanconf.py`.

We suggest explicitly setting `FAVICON_OUTPUT_PATH` in
`pelicanconf.py` and then copy the following definitions, or doing
something equivalently:

    SITELOGO   = FAVICON_OUTPUT_PATH + '/' + 'favicon.png'
    FAVICON    = FAVICON_OUTPUT_PATH + '/' + 'favicon.png'
    FAVICON_IE = 'favicon.ico'
    TOUCHICON  = FAVICON_OUTPUT_PATH + '/' + 'apple-touch-icon.png'


TODOs and BUGs
--------------

  * The use of `pngcrush` could and should be made optional, and
    `optipng` made an alternative. Or perhaps we should leave
    optimizing PNG image files to a separate plugin?

  * We could use `cairosvg` or a custom `pycairo` based method to
    convert the SVG file into PNG files without running an external
    tool like `inkscape`.

  * There may be a Python library to generate ICO files (pillow?)
    which could allow us to avoid running the external `icotool` tool.

  * The way we run the external tools appears to rely on `subprocess`
    features introduced in Python 3.3.

  * Does our Python code run in Python 2?

  * Using `print(…)` to print debug output and the `logging` module is
    done inconsistently, to say the least.

  * There is no test suite yet.

  * Test the favicon usage in Pelican themes other than
    `pelican-bootstrap3` and how `ndim_pelican_favicon` can help
    there.

There are probably more problems, but this should be a good list to
start with.
