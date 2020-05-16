===============================
Setup
===============================

For this project, we're going to want to have a project folder and a virtual
environment set up. Follow along and we'll get that set up.

.. note:: Before continuing, if you're new to software development, you
   should pick a directory or folder on your computer to save your project. A
   common name for this directory is ``src``. It can live anywhere you like. You
   should copy the path from your file explorer and hold on to it, we're going
   to use it later.  We reference this path as ``/path/to/src/``.

So the first thing you need to do is open your terminal.

.. tabs::

   .. group-tab:: Windows

      On Windows, there are two terminals: cmd and powershell. If you're not
      sure which to pick, choose cmd. Future directions are written with this
      terminal in mind.

   .. group-tab:: MacOS

      The MacOS default terminal is just called Terminal.

   .. group-tab:: Ubuntu

      (fill out later)

With your terminal open, you're going to want to navigate to the
``/path/to/src/``. After that, we'll set up a project directory, and then
navigate into it. In the commands below, replace ``/path/to/src/`` with your
specific path you saved earlier. The name ``virtual-tennis`` is a nice
descriptive name for your project folder, but you can change the name if you'd
like.

.. warning:: Each of these steps has multiple commands. Make sure to enter them
   one at a time and hit the enter or return key and wait until they stop
   putting new text on the screen before the next command.

On all systems:

.. code-block::

   cd /path/to/src/
   mkdir virtual-tennis
   cd virtual-tennis

Our next step is to set up a virtual environment. We're going to use the python
library ``venv`` for this. After creating it, we need to activate it, and
install ``ppb``. Below, we call our virtual environment ``.venv``, but this is
only one of many possible names. If you change the name, replace it in following
commands with your new name. The structure in a virtual environment doesn't
change based on its name.

.. note:: A virtual environment is a way to isolate the requirements of your
   project from other Python projects on your computer. This lets you have
   projects with conflicting requirements, like two different versions of
   ``ppb``.

.. tabs::

   .. group-tab:: Windows

      .. code-block::

         py -3.8 -m venv .venv
         .venv\Scripts\activate
         python -m pip install ppb

   .. group-tab:: MacOS

      .. code-block::

         python3.8 -m venv .venv
         source .venv/bin/activate
         python -m pip install ppb

   .. group-tab:: Ubuntu

      (add later)

The last step will depend on the code editor you've picked. If you're using an
IDE (PyCharm, VSCode, or similar) you'll want to open your project in your IDE.

If you're using a plain text editor (GEdit, Notepad++) open it, but don't create
any files yet.

Keep your terminal open, you're going to use it later. If you close it, you
should navigate back to your project folder and activate the virtual environment
again.

With all of this out of the way, we can move on to our first step: Creating a
window.
