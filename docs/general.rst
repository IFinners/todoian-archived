=========================
General Usage Information
=========================

Synonyms
========

All commands have shorter synonyms, for example 'a' can be used instead or 'add', and once a synonym is mentioned one can assume it works for any given example even if not explicitly stated.


Positional Arguments
====================

Commands work with positional arguments rather than arguments defined by keywords. This means the order and spacing of commands is crucial.

Instead of writing something like:
::

   add desc="description here" date=2018-01-01 repeat=7

Simply write:
::

   add "New Task Description" 2018-01-01 7
   
In order to leave an optional command as default but set one positioned further to the right, simply leave that position entirely blank and remember the importance of spacing. For example, setting only the repeat of the task above would require the following command:
::

   add "New Task Description"  7
   
Take note of the double space between the task description and the repeat.

The Two Types of Optional Arguments
===================================

Optional arguments are shown by square brackets ([]) or curly brackets ({}) throughout this command guide.
Arguments in square brackets, if not given, will be asked for through a seperate prompt before the operation can be
completed whereas ones in curly brackets will be automatically set to a default - for example:
::

   add ["New Task Description"] {Date} {Repeat}

The user will be prompted for a task description if one isn't provided but both the Date and the Repeat will be
set to their default values - today's date and no repeat respectively.
   