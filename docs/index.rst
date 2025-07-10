Podium
======

A presentation tool for developers.

Quickstart
----------

In your virtualenv, install Podium, and then run it::

    $ pip install podium
    $ podium

This will pop up a GUI window.

Problems under Ubuntu/Debian
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Debian and Ubuntu's packaging of Python omits the ``idlelib`` library from it's
base packge. If you're using Python 2.7 on Ubuntu 13.04, you can install
``idlelib`` by running::

    $ sudo apt-get install idle-python2.7

For other versions of Python, Ubuntu and Debian, you'll need to adjust this as
appropriate.

Problems under Windows
~~~~~~~~~~~~~~~~~~~~~~

If you're running Podium in a virtualenv, you'll need to set an
environment variable so that Podium can find the TCL graphics library::

    $ set TCL_LIBRARY=c:\Python27\tcl\tcl8.5

You'll need to adjust the exact path to reflect your local Python install.
You may find it helpful to put this line in the ``activate.bat`` script
for your virtual environment so that it is automatically set whenever the
virtualenv is activated.

Documentation
-------------

Documentation for Podium can be found on `Read The Docs <http://podium-app.readthedocs.org>`__.

Community
---------

Podium is part of the `BeeWare suite <https://beeware.org>`__. You can talk to the
community through:

* `@beeware@fosstodon.org on Mastodon <https://fosstodon.org/@beeware>`__

* `Discord <https://beeware.org/bee/chat/>`__

We foster a welcoming and respectful community as described in our `BeeWare Community
Code of Conduct <https://beeware.org/community/behavior/>`__.

Contributing
------------

If you experience problems with Podium, `log them on GitHub <https://github.com/beeware/podium/issues>`__.

If you want to contribute, please `fork the project <https://github.com/beeware/podium>`__ and `submit a pull request <https://github.com/beeware/podium/pulls>`__.


Contents:

.. toctree::
   :maxdepth: 2
   :glob:

   internals/contributing
   internals/roadmap
   releases


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
