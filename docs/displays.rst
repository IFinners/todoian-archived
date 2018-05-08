==================================
Display and Miscellaneous Commands
==================================

Todoian customises its display based upon the command it has just been given, but the various types of display can also be invoked through their own set of commands.


The List Command
================

The main display command is the list (ls, list) command which unadorned prints any Overdue tasks and Tasks due Today. Additions to the list command can do the following:

View all tasks with due dates of today with (t, today):
::

   list today

All overdue tasks with (o, overdue):
::

 list overdue

Task's due tomorrow with (tm, tomorrow):
::

   list tomorrow

Task's due tomorrow and beyond with (f, future):
::

   list future

All Goals with (g, goals):
::

   list goals

By default, Goals are displayed without their Subgoals being printed but merely indicated by a trailing ellipsis ('...').
Goals, and all of their Subgoals, can be viewed with (gs, goals-subs):
::

   list goals-subs

All Goals (without Subgoals) and Tasks can be viewied with (a, all):
::

   list all

And any Task or Goal with a specific Tag can be viewed with (tg, tag):
::
   
   list tag [tag]


The View Commands
=================

There are two other displays available but these aren't prompted by list but rather view.

A single Goal and all of its Subgoals can be viewed with (vg, view-goal):
::

   view-goal goal-number

All tags associated with a Task or Goal can be viewed with (vt, view-tags) for Tasks and (vgt, view-goal-tags) for Goals:
::

   view-tags task-number


Other Commands
==============

A link to this documentation can be displayed within the program with (h, help)
::

  help
