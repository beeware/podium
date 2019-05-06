Contributing to Podium
======================


If you experience problems with Podium, `log them on GitHub`_. If you want to contribute code,
please `fork the code`_ and `submit a pull request`_.

.. _log them on Github: https://github.com/pybee/podium/issues
.. _fork the code: https://github.com/pybee/podium
.. _submit a pull request: https://github.com/pybee/podium/pulls


Setting up your development environment
---------------------------------------

Install prerequisites
~~~~~~~~~~~~~~~~~~~~~

Podium requires Toga A Python native, OS native GUI toolkit. Follow the instructions
to install `Toga Prerequisites`_ for your operating system.

Setup virtual environment and install Podium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The recommended way of setting up your development environment for Podium
is to install a virtual environment, install the required dependencies and
start coding. Assuming that you are using ``virtualenvwrapper``, you only have
to run::

    $ git clone https://github.com/beeware/podium.git
    $ cd podium
    $ mkvirtualenv podium

Podium uses ``unittest`` for its own test suite as well as additional helper
modules for testing. To install Podium in development mode, you have to run the
following command within your virtual environment::

    $ pip install -e .


Now you are ready to start hacking! Have fun!

.. _Toga Prerequisites: https://github.com/beeware/toga#prerequisites
