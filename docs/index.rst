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

Documentation for Podium can be found on `Read The Docs`_.

Community
---------

Podium is part of the `BeeWare suite`_. You can talk to the community through:

 * `@pybeeware on Twitter`_

 * The `BeeWare Gitter channel`_, for discussing the development of new features in the BeeWare suite, and ideas for new tools for the suite and questions about how to use the BeeWare suite.


.. _BeeWare suite: http://pybee.org
.. _Read The Docs: http://podium-app.readthedocs.org
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _BeeWare Gitter channel: https://gitter.im/pybee/general

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
