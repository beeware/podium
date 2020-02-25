.. image:: https://beeware.org/project/projects/applications/podium/podium.png
    :width: 72px
    :target: https://beeware.org/project/projects/applications/podium

Podium
======

.. image:: https://badges.gitter.im/beeware/general.svg
   :target: https://gitter.im/beeware/general


A markup-based slide presentation tool.

Why?
----

Developers go to conferences. And when they do, they need slide decks.

Unfortunately, while presentation tools like `Keynote`_ and `PowerPoint`_
are great for business presentations, they aren't well suited to the
needs of developers. The mainstay of developer presentations -- code
samples -- are generally painful to add to a Keynote presentation.

These presentation tools also come from a WYSIWYG (What You See Is What You
Get) tradition. This can be powerful, because it makes it easy to put
anything you want onto a slide. But it can also be painful, because you
end up spending all your time pushing pixels into the right place, instead
of focussing on the content of your talk. And if you want to make a style
change, you may need to apply that change manually to every slide. The lessons
of separating content from markup can't be applied to a WYSIWYG world.

On top of all that, the document formats for Keynote and Powerpoint are
binary blobs -- they don't lend themselves to version control, collaborative
editing, and so on.

The developer response to this has been to use HTML5. Recent years have seen
the development of a number of HTML-based presentation tools, like prezi_,
`deck.js`_, `keydown`_ and `showoff`_. These tools exploit the power of HTML5
to make full screen presentations.

However, by using browser technology as the basis for these tools, they miss
one very important feature of WYSIWYG presentation tools: presenter mode.
One of the big features of Keynote and Powerpoint is that they aren't just
decks of slides -- they have presenter notes and timing tools, and the
display shown to the audience isn't the same as the display shown to the
presenter. Web-based presentation tools are often missing presenter mode.

Or, if they *do* have a presenter mode, they rely on you being able to
independently resize two separate web browsers, and they won't provide any
assistance in hiding all the browser toolbars, menus, titlebars, and so on.
This can be done, but it's awkward.

Many of these tools are also online-only. They assume that you have a good WiFi
connection, and will be able to display your content live off the internet...
which if you've ever been to a developer conference, you'll know is a risky
proposition.

Podium attempts to bridge the gap between these two poles. It is comprised of:

* A simple, text-based markup format, focussed on the needs of developer
  presentations.
* A graphical presentation tool that has a presenter display independent of
  the slide display.

.. _prezi: http://prezi.com
.. _deck.js: http://imakewebthings.com/deck.js/
.. _keydown: https://github.com/infews/keydown
.. _showoff: https://github.com/drnic/showoff

Quickstart
----------

Official releases of Podium can be downloaded from the `GitHub releases page
<https://github.com/beeware/podium/releases>`__.

Download the binary for your platform of choice, and run it. This should open a
file dialog, prompting you to open a ``.podium`` slide deck. An example Podium
slide deck is also available in the releases folder. Unzip the deck, and open
it in Podium.

.. note::

    The Linux AppImage format is a cross-platform binary that should run on
    any Linux distribution using GLibC 2.23 or later - this includes Ubuntu
    16.04 and later, Fedora 24 and later, and others.

    After downloading the AppImage, you may need to mark the AppImage file as
    executable (``chmod +x Podium-*.AppImage``) first. In Linux, ``.podium``
    files appear as directories; select the directory and click ``Open``.

Controls from here are keyboard based:

* CMD-P - Enter presentation mode; or, if in presentation mode, Pause timer
* Esc - Exit presentation mode
* CMD-Tab - Switch displays
* Right/Left arrows - Next/previous slide
* Down/Up arrows - Next/previous slide
* Enter - Next slide
* Home/End - first/last slide
* CMD-A - Switch aspect ratio between 16:9 and 4:3
* CMD-R - Reload slide deck
* CMD-T - Reset timer

If you're on Linux, "CMD" is the Control key.

Developing Podium
-----------------

Podium uses the `BeeWare <https://beeware.org>`__ suite of tools and libraries -
most notably, the `Toga <https://github.com/beeware/toga>`__ widget toolkit, and
the `Briefcase <https://github.com/beeware/briefcase>`__ packaging tool.

To develop Podium, create a virtual environment, and install the BeeWare tools.

If you're using Linux, you'll need to install some system packages first::

    # Ubuntu/Debian
    $ sudo apt-get update
    $ sudo apt-get install python3-dev libgirepository1.0-dev libcairo2-dev libpango1.0-dev libwebkit2gtk-4.0-37 gir1.2-webkit2-4.0

    # Fedora
    $ sudo dnf install pkg-config python3-devel gobject-introspection-devel cairo-devel cairo-gobject-devel pango-devel webkitgtk3


Then, you can create a virtual environment and install the BeeWare tools::

    $ mkdir beeware
    $ cd beeware
    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install --pre beeware

Now that you have the code, you can clone the Podium repository and run it in
developer mode::

    (venv) $ git clone https://github.com/beeware/podium.git
    (venv) $ cd podium
    (venv) $ briefcase dev

This should open the same file dialog as before.

Packaging with Briefcase
~~~~~~~~~~~~~~~~~~~~~~~~

Use `Briefcase`_ to package this repository as a standalone application::

    $ briefcase package

Depending on your platform, this will produce a ``macOS`` folder containing
a Podium DMG file, or a ``linux`` folder containing a ``.AppImage`` file.

.. note::

    Packaging cross-distribution Linux binaries is a complex process; See `the
    notes on AppImage packaging
    <https://briefcase.readthedocs.io/en/latest/reference/platforms/linux/appimage.html>`__
    in the Briefcase documentation for more details.

Overriding Default themes
-------------------------

Define a `style.css` file to override the default theme. You can use the
**Debugging** section to help you create a theme that suites your style.

Debugging
---------

If you need to debug the CSS for a slide, you may want to use the "inspect
element" feature of the webview. You may need to enable manually enable the
feature at an operating system level:

* **macOS**: at a terminal prompt, run
  `defaults write NSGlobalDomain WebKitDeveloperExtras -bool true`

Documentation
-------------

Documentation for Podium can be found on `Read The Docs`_.

Community
---------

Podium is part of the `BeeWare suite`_. You can talk to the community through:

* `@pybeeware on Twitter`_

* The `beeware/general`_ channel on Gitter.

We foster a welcoming and respectful community as described in our
`BeeWare Community Code of Conduct`_.

Contributing
------------

If you experience problems with Podium, `log them on GitHub`_. If you
want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _BeeWare suite: https://beeware.org/
.. _Keynote: https://en.wikipedia.org/wiki/Keynote_(presentation_software)
.. _PowerPoint: https://en.wikipedia.org/wiki/Microsoft_PowerPoint
.. _Briefcase: https://github.com/beeware/briefcase
.. _Read The Docs: https://podium-app.readthedocs.io/en/latest/
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _beeware/general: https://gitter.im/beeware/general
.. _BeeWare Community Code of Conduct: https://beeware.org/community/behavior/
.. _log them on Github: https://github.com/beeware/podium/issues
.. _fork the code: https://github.com/beeware/podium
.. _submit a pull request: https://github.com/beeware/podium/pulls
