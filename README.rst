Podium
======

A markup-based slide presentation tool.

Why?
----

Developers go to conferences. And when they do, they need slide decks.

Unfortunately, while presentation tools like Keynote_ and PowerPoint_
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

However, by using browser technology as the basis for these tools, they miss one
very important feature of WYSIWYG presentation tools: presenter mode.

One of the big features of Keynote and Powerpoint is that they aren't just
decks of slides -- they have presenter notes and timing tools, and the
display shown to the audience isn't the same as the display shown to the
presenter.

Many of these tools also assume that you have a good WiFi connection, and will
be able to display your content live off the internet... which if you've ever
been to a developer conference, you'll know is a risky proposition.

Podium attempts to bridge the gap between these two poles. It is comprised of:

* A simple, text-based markup format, focussed on the needs of developer
  presentations.
* A graphical presentation tool that has a presenter display independent of
  the slide display.

.. Keynote: https://www.apple.com/au/iwork/keynote/
.. PowerPoint: http://office.microsoft.com/en-au/powerpoint/
.. _prezi: http://prezi.com
.. _deck.js: http://imakewebthings.com/deck.js/
.. _keydown: https://github.com/infews/keydown
.. _showoff: https://github.com/drnic/showoff

Quickstart
----------

To install podium::

    $ pip install podium

Then, you can run podium on a presentation::

    $ podium my-presentation

Presentations are directories containing content.

This will pop up 2 GUI windows, both displaying a test pattern. Controls from here are keyboard
based:

* F8 - Go to full screen presentation mode
* F4 - Switch displays for the slide and presenter
* Right/left arrows - next/previous slide
* Command-right/left arrows - first/last slide

Documentation
-------------

Documentation for Podium can be found on `Read The Docs`_.

Community
---------

Podium is part of the `BeeWare suite`_. You can talk to the community through:

 * `@pybeeware on Twitter`_

 * The `BeeWare Users Mailing list`_, for questions about how to use the BeeWare suite.

 * The `BeeWare Developers Mailing list`_, for discussing the development of new features in the BeeWare suite, and ideas for new tools for the suite.

Contributing
------------

If you experience problems with Podium, `log them on GitHub`_. If you
want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _BeeWare suite: http://pybee.org
.. _Read The Docs: http://podium-app.readthedocs.org
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _BeeWare Users Mailing list: https://groups.google.com/forum/#!forum/beeware-users
.. _BeeWare Developers Mailing list: https://groups.google.com/forum/#!forum/beeware-developers
.. _log them on Github: https://github.com/pybee/podium/issues
.. _fork the code: https://github.com/pybee/podium
.. _submit a pull request: https://github.com/pybee/podium/pulls
