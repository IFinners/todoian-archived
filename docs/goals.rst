=============
Goal Commands
=============

Goals have many of the commands that Tasks do and can usually be invoked in the same way with the command slightly modified with either the letter 'g' or the word 'goal'.

Adding
======
(g, ag, add-goal)

::

   add ["New Goal Description"] {Target} {Percent Complete}
   
The Goal description must be surrounded by double-quotes, and the percentage must be an integer between 0 and 100.


Completing
==========
(cg, complete-goal)

Marking a Goal as complete moves it from the active Goal list to an unseen cache:
::

   complete goal-number


Deleting
========
(dg, delg, delete-goal)

Deleting a Goal is functionally equivalent to completing a Goal, only the cache list differs:
::

   delete goal-number
   
All Tasks can be deleted by writing 'a' or 'all' instead of a Goal number:
::

   delete all


Undoing a Completion or Deletion
================================
As long as the program hasn't been exited since a completion or deletion was made, the Goal's can be restored to 
their previous state using the commands:

ucg, uncheck-goal - for undoing a completion

ug, undo-goal -  for undoing a deletion

Both of these commands will work for the restoration of multiple items


Moving
======
(mg, mvg, move-goal)
Goals aren't sorted by any of their parameters, and as such the ordering of them is left entirely up to the user who can change the order at any time using the following:
::

   move-goal goal-number {move-number}

Where the move number is the position to move the goal to in the list. If the move number is not provided the user will be prompted for one.


Editing a Description
=====================
(eg, edg, edit-goal)
Editing a Goals's description can be done through the following command:
::

   edit goal-number [goal description]

Note that there is no need to encase the Goal description in quotation marks unlike with the add command.


Changing a Target
=================
(ct, change-target)
A Goal's target is similar to a Tasks due-date, but is entirely optional with no functionality depending upon it. 
Target's can be anything from concrete dates to vague statements like 'Before the end of Summer' and can be added by using the following command:
::

   change-target goal-number [new target]


Changing a Percentage
=====================
Beneath is Goal is a progress bar indicating how close the Goal is to being complete - this is where the percentage 
comes in. By default, percentages are set to 'auto', allowing the number of subgoals completed and still to do 
determine the percentage completion, but custom percentages can be added using the following command:
::

   change-percentage goal-number [percentage]

Note that in order to restore the default 'auto' percentage setting one simply has to enter 'auto'(without the quotes) as the value either on the command line or at the prompt.


Adding a Tag
============
(agt, add-goal-tag)
Tagging a Goal with a keyword means it can be displayed with other Tasks and goals (see the Display Command section of 
this guide) that share that tag. To add tag(s) to a Goal, 
enter the following command:
::

   add-goal-tag goal-number [tag,tag2,tag3]


Removing a Tag
==============
(rgt, remove-goal-tag)
A specific tag can be removed using it as the keyword in the command to follow, or all tags for that Goal can be 
removed by using the keyword 'all':
::

   remove-tag goal-number keyword
