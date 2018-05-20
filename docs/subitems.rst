.. _subitem:

================
Subitem Commands
================

Both Tasks and Goals can be broken down into smaller parts through the use of Subitems. The functionality is identical
for Tasks and Goals but the commands vary slightly as indicated beneath each section below.

Adding
======
(s, subtask) (sg, subgoal)

::

   subtask task-number [subitem description]


Completing
==========
(cs, complete-sub) (csg, complete-subgoal)

Marking a Subitem as complete strikesthrough the subitem when displayed, updates a Goal's progress bar if percentage 
is set to 'auto' and, upon the completion of all Subitems, prompts for the optional completion of the Item iself. 
::

   complete goal-number


Undoing a Completion
====================
(us, uncomplete-sub) (usg, uncomplete-subgoal)

Undoing a Subitem completion removes the strikethorugh and alters a Goal's progress if the percentage 
is set to 'auto'.
::

   uncomplete-sub task-number [subtask-number]


Deleting
========
(ds, delete-subtask) (dsg, delete-subgoal)

Unlike the deletion of a Task or Goal, the deletion of a Subitem is permanent.
::

   delete task-number [subtask-number]
   

Moving
======
(ms, move-subtask) (msg, move-subgoal)

Subitems can't be transferred to another item, but their order beneath the Task or Goal can be changed.
::

   move-subtask task-number subtask-number [new-position]


Editing a Description
=====================
(es, edit-subtask) (esg, edit-subgoal

::

   edit-subtask task-number subtask-number [new subtask description]

Note that there is no need to encase the Subtask description in quotation marks.
