.. image:: https://beeware.org/project/projects/applications/podium/podium.png
    :width: 72px
    :target: https://beeware.org/project/projects/applications/podium

Podium
======

.. image:: https://img.shields.io/discord/836455665257021440?label=Discord%20Chat&logo=discord&style=plastic
   :target: https://beeware.org/bee/chat/
   :alt: Discord server

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

Controls from here are keyboard based:

* CMD-Shift-P - Enter presentation mode; or, if in presentation mode, Pause timer
* CMD-P - Open presentation in Print view
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
    $ sudo apt-get install python3-dev libgirepository2.0-dev libcairo2-dev libpango1.0-dev gir1.2-gtk-3.0 libcanberra-gtk3-module gir1.2-webkit2-4.1 dpkg-dev

    # Fedora
    $ sudo dnf install pkg-config python3-devel gobject-introspection-devel cairo-devel gtk3 cairo-gobject-devel pango-devel libcanberra-gtk3 webkit2gtk4.1 rpm-build


Then, you can create a virtual environment and install the BeeWare tools::

    $ mkdir beeware
    $ cd beeware
    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install briefcase

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

Depending on your platform, this will produce a ``macOS`` folder containing a
Podium DMG file, or a ``linux`` folder containing a system package appropriate
to your distribution (a `.deb`, `.rpm` or `.pkg.zip` file)

Overriding Default themes
-------------------------

Define a `style.css` file to override the default theme. You can use the
**Debugging** section to help you create a theme that suites your style.

Debugging
---------

If you need to debug the CSS for a slide, you may want to use the "inspect
element" feature of the webview. You may need to enable manually enable the
feature at an operating system level:

* **macOS**: at a terminal prompt, run:

    defaults write org.beeware.podium WebKitDeveloperExtras -bool true

Documentation
-------------

Documentation for Podium can be found on `Read The Docs`_.

Community
---------

Podium is part of the `BeeWare suite`_. You can talk to the community through:

* `@pybeeware on Twitter`_

* `Discord <https://beeware.org/bee/chat/>`__

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
