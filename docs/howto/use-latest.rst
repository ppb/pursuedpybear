Test Pre-Release Features
===========================================================

Sometimes you want to try the latest features that have been developed for
ppb before they have a formal release on pypi. You have two options: provide
a git uri to the ppb canon branch or use a dev release from `test.pypi.org`_.

With pip Directly
----------------------------------------

To install with pip directly from github, enter the following command into your shell::

   pip install git+https://github.com/ppb/pursuedpybear.git

If you want to use the test server for pypi instead::

   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple --pre ppb

With requirements.txt
-----------------------------------------

To install using a requirements.txt file and the current git code, put
``git+https://github.com/ppb/pursuedpybear.git`` as your requirement line
then invoke pip as normal::

   pip install -r requirements.txt

To install from test.pypi.org with a requirements file, put the following in
your requirements.txt::

   --index-url https://test.pypi.org/simple/
   --extra-index-url https://pypi.org/simple
   --pre
   ppb

These options download ppb from `test.pypi.org`_ and the remaining
dependencies from PyPI as normal.

Now you need to invoke pip as so::

   pip install -r requirements.txt


.. _test.pypi.org: https://test.pypi.org/
