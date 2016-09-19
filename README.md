ndim-pelican-favicon
====================

From the original SVG file containing the favicon, generate
`favicon.ico` and an assortment of PNG files.


Configuration
-------------

`ndim-pelican-favicon` defines a number of its own configuration variables:

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

Stock Pelican configuration variables also used by `ndim-pelican-favicon`:

  * `PATH`

    Location of the source files.

  * `OUTPUT_PATH`

    Location of the output files.

Other settings which need to work together with the `FAVICON_*`
settings:

    SITELOGO   = FAVICON_OUTPUT_PATH + '/' + 'favicon.png'
    FAVICON    = FAVICON_OUTPUT_PATH + '/' + 'favicon.png'
    FAVICON_IE = 'favicon.ico'
    TOUCHICON  = FAVICON_OUTPUT_PATH + '/' + 'apple-touch-icon.png'


Bugs
----
