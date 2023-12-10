===============================
Virtual Tennis
===============================

.. toctree::
   :hidden:
   :maxdepth: 0
   :titlesonly:

   setup
   window
   ball

In this tutorial, we're going to build a game virtual tennis game in the vein
of Pong_. We're going to go through the whole process: planning our approach,
breaking out individual tasks, setting up our environment, and coding.

Before you start writing code on a project, it's best to think about the game
we're trying to make. For research, go try `this implementation of
Pong <https://archive.org/details/PONGV2.11996DJTAction>`_ on the internet
archive.

Let's think about what's going on in this version:

#. It opens on a menu with sample play happening in the background.
#. The menu explains all the controls.
#. When you start a one player game, you receive control of one of the paddles.
#. The ball launches, and you need to move up and down to deflect the ball.
#. The ball bounces off the top and bottom walls.
#. If either of you miss the ball, the other player's score goes up.
#. If a player reaches 15 points, the game ends with fanfare and the word
   "Winner!" printed repeatedly on that side of the screen.
#. Then it goes back to the menu.

Now that we've looked at an example of our project, let's identify the
important parts:

* The core game play is a ball and two paddles, each controllable by a player.
* The ball needs to be able to bounce off the top and bottom wall and either
  paddle.
* The paddles need to be able to move.
* We need to be able to track the score.
* We need to be able to end the game.

This tutorial will break each of these requirements into smaller pieces so we
can test features as we go.

Before we get started, you'll need a few things done first:

#. Install python 3.8 on your system. We suggest installing from python.org for
   best results. For more information, see the
   `Django Girls tutorial <https://tutorial.djangogirls.org/en/installation/#python>`_.
   for more specific instructions on installation.
#. Install a code editor. We suggest PyCharm, Sublime Text, GEdit or VSCode.
   Extra information and suggestions can be found at
   `Django Girls <https://tutorial.djangogirls.org/en/installation/#code-editor>`_.
#. You'll also need to know the basics of Python. Again, Django Girls has a
   great `tutorial <https://tutorial.djangogirls.org/en/python_introduction/>`_
   for this.

Once you have those things done, you can move on to our first step: setting up
our project.


( The following will be deleted before final publication.)

2. A ball that bounces on the edges of the screen.
3. A player paddle that can be moved.
4. Collision between player paddle and ball.
5. A score board tracking how many times the player hits the far side of the
   screen.
6. Removing the ball from play when it hits the far wall.
7. Launching the ball with a key press.
8. Removing the ball if it hits the player's wall.
9. Adding a second player paddle.
10. Adding a new score board for second player.
11. End the game.
12. Ideas for making the game your own.
