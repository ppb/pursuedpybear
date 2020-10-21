Test Pre-Release Features
===========================================================

Sometimes you want to try the latest features that have been developed for
ppb before they have a formal release on pypi. You have two options: provide
a git uri to the ppb canon branch or use a dev release from test.pypi.org.

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

To install from test.pypi.org with a requirements file, put ``ppb`` in your
requirements file as normal, then invoke pip as so::

   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple --pre -r requirements.txt
