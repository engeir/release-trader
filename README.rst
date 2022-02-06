Release Trader
==============

|Python Version| |License|

|Read the Docs| |Tests|

|pre-commit| |Black|

.. |Python Version| image:: https://img.shields.io/pypi/pyversions/release-trader
   :target: https://pypi.org/project/release-trader
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/release-trader
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/release-trader/latest.svg?label=Read%20the%20Docs
   :target: https://release-trader.readthedocs.io/
   :alt: Read the documentation at https://release-trader.readthedocs.io/
.. |Tests| image:: https://github.com/engeir/release-trader/workflows/Tests/badge.svg
   :target: https://github.com/engeir/release-trader/actions?workflow=Tests
   :alt: Tests
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


    This project is largely abandoned, but I'm keeping it around for anyone who wants
    to make a forked version of it. It is capable of checking Binance and Coinbase for
    new coins and trade them on gate.io, but selling them with either a stop loss or as
    they increase in value by ten percent is not being handled properly.

    `This repository`_ basically follow the same strategy, except is uses only Binance.


Features
--------

* Opens a new trade on gate.io when a new release is published on either
  Binance or Coinbase.
* Automatically trades back to BTC when the new coin has increased its value by ten
  percent, with a stop loss of one percent.


Installation
------------

It has not yet been published on PyPI_, so to install you should use poetry_:

.. code:: console

    $ poetry install

You should then create a file based on the example in ``.user.cfg.example`` and name it
`.user.cfg``.`

You can install *Release Trader* via pip_ from PyPI_:

.. code:: console

   $ pip install release-trader


Usage
-----

Please see the `Command-line Reference <Usage_>`_ for details.


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_,
*Release Trader* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/engeir/release-trader/issues
.. _pip: https://pip.pypa.io/
.. _This repository: https://github.com/CyberPunkMetalHead/gateio-crypto-trading-bot-binance-announcements-new-coins
.. _poetry: https://www.python-poetry.org/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://release-trader.readthedocs.io/en/latest/usage.html
