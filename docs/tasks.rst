=============
Task Commands
=============

Ordered by their due dates and customisable with repeats, tags and Subitems(see :ref:`Subitem Commands <subitem>` for details) 
Tasks are what Task Managers... well... manage and here is a breakdown of how to do just that.

Adding
======
(a, add, add-Task)

::

   add ["New Task Description"] {Date} {Repeat}
   

- The Task description must be surrounded by double-quotes.
- The date must be in one of the formats detailed in the :ref:`change-date` section.
- The repeat must be one of the options detailed in the :ref:`add-repeat` section.


Completing
==========
(c, comp, complete)

Marking a Task as complete moves it from the active Task list to an unseen cache, unless it has a repeat in which case 
it is added back onto the Task list with the appropriate new information.
::

   complete task-number

All Tasks with due dates equal to the current date are marked as complete by writing 't' or 'today' instead of a Task number:
::

   complete today

All Tasks with due dates earlier than the current date are marked as complete by writing 'o' or 'overdue' instead of a Task number:
::

   complete overdue

Note that this completes overdue tasks with repeats until their due date is no longer overdue.  


Deleting
========
(d, del, delete)

Deleting a Task is similar to completing one in that it moves the Task from the active Task list to an unseen cache. 
However, with deletion this is done regardless of any repeat flags.
::

   delete task-number
   
All Tasks can be deleted by writing 'a' or 'all' instead of a Task number - a prompt will ask for confirmation:
::

   delete all


Undoing a Completion or Deletion
================================
As long as the program hasn't been exited since a completion or deletion was made, the items can be restored to their previous state using the commands:

uncheck, uc - for undoing a completion

undo, u -  for undoing a deletion

Both of these commands will work for the restoration of multiple items


Moving
======
(m, mv, move)

Tasks are sorted by their due dates, and whilst this cannot be changed, the order of Tasks within their date brackets 
can with the following command:
::

   mv task-number [move-number]

Where the move number is the position to move the Task to in the list.


Editing a Description
=====================
(e, ed, edit)

Editing a Task's description can be done through the following command:
::

   edit task-number [new Task description]

Note that there is no need to encase the Task description in quotation marks unlike with the add command.


.. _change-date:

Changing a Due Date
===================
(cd, change-date)

Changing a Task's due date can be done through the prompt that follows the following command:
::

   change-date task-number [due date]

The date can be entered as:

- A date formatted like YYYY-MM-DD e.g. 2018-01-25:
- An abbreviated day name (e.g. wed) would set the date to the next Wednesday from today's date.
- 't', which sets the due date to today, or 'tm' which sets the due date to tomorrow's date.


.. _add-repeat:

Adding a Repeat
===============
(ar, add-repeat)

Repeats allow Tasks to be automatically re-added to the Task list upon completion. The repeat can be set with the following command:
::

   add-repeat task-number [repeat]

There are four different types of repeat that can be set. The simplest of these is the number of days repeat - 
for example setting the repeat to the value 7 will result in a Task that repeats weekly.

Another way to specify a repeat is through a three letter day name or a list of day names (of any length) seperated 
by a comma:
::

   add-repeat task-number mon,wed,fri

This Task would repeat every Monday, Wednesday and Friday. Note that one of the named repeat days must be equal 
to the current due date or there will be an error upon completion of the Task.

Similarly, a list of dates can be used for the repeats:
::

   add-repeat task-number 2018-01-01,2018-02-01,2018-03-01

This Task would, once initially completed, have its due date changed to the 1st of February and then, once completed 
again, the 1st of Match.

Finally, a Task can be set with a repeat spanning any number of months provided the date of the day for the repetition 
to occur is no higher than the 28th by using the following command structure:
::

   add-repeat task-number 3m

This Task would repeat every 3 months on the day definied by its due date at the time of completion.


Removing a Repeat
=================
(rr, remove-repeat)

A repeat can be overwritten by using the add repeat command detailed above, or removed entirely with the following:
::

   remove-repeat task-number


Adding a Tag
============
(at, add-tag)

Tagging a Task with a keyword means it can be displayed with other Tasks and goals (see the Display Command section of this guide) that share that tag. To add tag(s) to a Task, enter the following command:
::

   add-tag task-number [tag,tag2,tag3]


Removing a Tag
==============
(rt, remove-tag)

A specific tag can be removed using it as the keyword in the command to follow, or all tags for that Task 
can be removed by using the keyword 'all':
::

   remove-tag task-number keyword


Viewing a tag
=============
(vt, view-tags)

To view a list of all of a Tasks tags use the following command:
::
   
   view-tags task-number
