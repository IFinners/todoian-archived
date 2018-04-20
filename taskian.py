#!/usr/bin/env python3

"""A Command Line Task Manager."""

import re
import pickle
from datetime import datetime as dt
from datetime import timedelta


def decide_action(command):
    """Decides which action the argument requires."""
    auto_display = True
    command_regex = re.search(r'^([-\w]*)\s?(.*)', command)
    command_main = command_regex.group(1).lower()
    command_extra = command_regex.group(2).lower()

    if command_main in ('ls','list'):
        if command_extra in ('t', 'today'):
            view_today()
        elif command_extra in ('o', 'overdue'):
            view_overdue()
        elif command_extra in ('tm', 'tomorrow'):
            view_tomorrow()
        elif command_extra in ('f', 'future'):
            view_tomorrow()
            view_future()
        elif command_extra in ('g', 'goals'):
            view_goals()
        elif command_extra in ('gs', 'goals-subs'):
            view_goals(show_subs=True)
        elif command_extra in ('a', 'all'):
            view_goals()
            smart_display()
        elif command_extra.startswith('tg') or command_extra.startswith('tag'):
            view_tag(command_extra)
        else:
            smart_display(mini=True)
        auto_display = False

    elif command_main in ('vg', 'view-goal'):
        print()
        view_goal(int(command_extra) - 1, subs=True)

    elif command_main in ('a', 't' 'add'):
        add_task(command_regex.group(2))

    elif command_main in ('g', 'ag', 'add-goal'):
        add_goal(command_regex.group(2))
        view_goals()
        auto_display = False

    elif command_main in ('rm', 'r', 'remove'):
        if command_extra in ("all", 'a'):
            check = input("  This Will Delete All Task Data. Are You Sure "
                          "You Want to Continue? (y/n): ")
            if check.lower() in ('y', 'yes'):
                task_data.clear()
            else:
                print("  Removal of All Tasks Aborted.")
        else:
            delete_item(int(command_extra) - 1, deleted_tasks)

    elif command_main in ('rg', 'rmg', 'remove-goal'):
        if command_extra in ("all", 'a'):
            check = input("  This Will Delete All Goal Data. Are You Sure "
                          "You Want to Continue? (y/n): ")
            if check.lower() in ('y', 'yes'):
                goal_data.clear()
            else:
                print("  Removal of All Goals Aborted.")
        else:
            delete_item(int(command_extra) - 1, deleted_goals)
            view_goals()
            auto_display = False

    elif command_main in ('c', 'complete'):
        if 't' in command_extra or 'today' in command_extra:
            complete_today()
        else:
            complete_task(int(command_extra) - 1)

    elif command_main in ('cg', 'complete-goal'):
        complete_goal(int(command_extra) - 1)
        view_goals()
        auto_display = False

    elif command_main in ('e', 'ed', 'edit'):
        edit_desc(command_regex.group(2), task_data)

    elif command_main in ('eg', 'edg', 'edit-goal'):
        edit_desc(command_regex.group(2), goal_data)
        view_goals()
        auto_display = False

    elif command_main in ('cd', 'change-date'):
        change_date(command_extra)

    elif command_main in ('ct', 'change-target'):
        change_target(command_regex.group(2))
        view_goals()
        auto_display = False

    elif command_main in ('cp', 'change-percentage'):
        change_percentage(command_extra)
        view_goals()
        auto_display = False

    elif command_main in ('ar', 'add-repeat'):
        add_repeat(command_regex.group(2))

    elif command_main in ('rr', 'remove-repeat'):
        remove_value(task_data, int(command_extra) - 1, 3)

    elif command_main in ('mv', 'm', 'move'):
        move_item(command_extra, task_data)

    elif command_main in ('mvg', 'mg', 'move-goal'):
        move_item(command_extra, goal_data)
        view_goals()
        auto_display = False

    elif command_main in ('mvs', 'ms', 'move-subtask'):
        move_sub(command_extra, task_data)

    elif command_main in ('mvsg', 'msg', 'move-subgoal'):
        move_sub(command_extra, goal_data)
        view_goals(show_subs=True)
        auto_display = False

    elif command_main in ('s', 'subtask'):
        add_sub(command_regex.group(2), task_data)

    elif command_main in ('sg', 'subgoal'):
        add_sub(command_regex.group(2), goal_data)
        view_goals(show_subs=True)
        auto_display = False

    elif command_main in ('cs', 'comp-subtask'):
        complete_sub(command_extra, task_data)

    elif command_main in ('us', 'uncomp-subtask'):
        uncomplete_sub(command_extra, task_data)

    elif command_main in ('usg', 'uncomp-subgoal'):
        uncomplete_sub(command_extra, goal_data)
        view_goals(show_subs=True)
        auto_display = False

    elif command_main in ('rs', 'remove-subtask'):
        delete_sub(command_extra, task_data)

    elif command_main in ('es', 'edit-subtask'):
        edit_sub(command_regex.group(2), task_data)

    elif command_main in ('csg', 'comp-subgoal'):
        complete_sub(command_extra, goal_data)
        view_goals(show_subs=True)
        auto_display = False

    elif command_main in ('rsg', 'remove-subgoal'):
        delete_sub(command_extra, goal_data)
        view_goals(show_subs=True)
        auto_display = False

    elif command_main in ('esg', 'edit-subgoal'):
        edit_sub(command_regex.group(2), goal_data)
        view_goals(show_subs=True)
        auto_display = False

    elif command_main in ('at', 'add-tag'):
        change_tag(command_regex.group(2), task_data)
        smart_display(mini=True)
        auto_display = False

    elif command_main in ('agt', 'add-goal-tag'):
        change_tag(command_regex.group(2), goal_data)
        smart_display(mini=True)
        auto_display = False

    elif command.lower() in ('u', 'undo'):
        undo_action(deleted_tasks)

    elif command.lower() in ('uc', 'uncheck'):
        undo_action(completed_tasks)

    elif command.lower() in ('ug', 'undo-goal'):
        undo_action(deleted_goals)
        view_goals()
        auto_display = False

    elif command.lower() in ('ucg', 'uncheck-goal'):
        undo_action(completed_goals)
        view_goals()
        auto_display = False

    elif command.lower() in ('h', 'help'):
        show_help()

    else:
        print("  Command Not Recognised - Try Again or "
              "Enter 'h' For Usage Instructions.")
    return auto_display


def view_today():
    """Prints all of today's tasks"""
    print()
    print('  ' + FONT_DICT['green'] + "TODAY'S TASKS" + FONT_DICT['end'], end='\n\n')
    empty = True
    for task in task_data:
        if task[2] == current_date:
            print("   {}".format(task[0]).rjust(6) + "| {}".format(task[1]))
            # Check for Subtasks
            if task[4]:
                print_sub(int(task[0] - 1), task_data)
            empty = False
    if empty:
        print("    No Tasks Found")
    print()


def view_tomorrow():
    """Prints all tasks due tomorrow"""
    print()
    print('  ' + FONT_DICT['orange'] + "TOMORROW'S TASKS" + FONT_DICT['end'], end='\n\n')
    empty = True
    for task in task_data:
        if ((dt.strptime(task[2], '%Y-%m-%d')
             - dt.strptime(current_date, '%Y-%m-%d')).days) == 1:
            print("    {}".format(task[0]).rjust(6) + "| {}".format(task[1]))
            # Check for Subtasks
            if task[4]:
                print_sub(int(task[0] - 1), task_data)
            empty = False
    if empty:
        print("    No Tasks Found")
    print()


def view_overdue():
    """Prints all overdue tasks."""
    print()
    print('  ' + FONT_DICT['red'] + "OVERDUE TASKS" + FONT_DICT['end'], end='\n\n')
    empty = True
    for task in task_data:
        if task[2] < current_date:
            over = ((dt.strptime(current_date, '%Y-%m-%d')
                     - dt.strptime(task[2], '%Y-%m-%d')).days)
            if over == 1:
                print("    {}".format(task[0]).rjust(6)
                      + "| {} [Due Yesterday]".format(task[1]))
            else:
                print("    {}".format(task[0]).rjust(6)
                      + "| {} [Due {} Days Ago]".format(task[1], over))
            # Check for Subtasks
            if task[4]:
                print_sub(int(task[0] - 1), task_data)
            empty = False
    if empty:
        print("    No Tasks Found")
    print()


def view_future():
    """Prints all future tasks to the terminal.."""
    print()
    print('  ' + FONT_DICT['blue'] + "FUTURE TASKS" + FONT_DICT['end'], end='\n\n')
    empty = True
    for task in task_data:
        if task[2] > current_date:
            until = ((dt.strptime(task[2], '%Y-%m-%d')
                          - dt.strptime(current_date, '%Y-%m-%d')).days)
            if until > 1:
                print("    {}".format(task[0]).rjust(6)
                      + "| {} [Due in {} Days]".format(task[1], until))
            # Check for Subtasks
                if task[4]:
                    print_sub(int(task[0] - 1), task_data)
                empty = False
    if empty:
        print("    No Tasks Found")
    print()


def view_goal(goal_num, subs=False):
    """Display an individual goal with optional subtask display."""
    goal = goal_data[goal_num]
    progress = goal[3]
    if progress == 'auto':
        percent_done = auto_percentage(goal[0] - 1) // 5
    else:
        percent_done = int(progress) // 5

    print("    {}".format(goal[0]).rjust(6), end='')
    if goal[2] and goal[4] and not subs:
        print("| {} [Target: {}]   ...".format(goal[1].upper(), goal[2]))
    elif goal[2] and not goal[4]:
        print("| {} [Target: {}]".format(goal[1].upper(), goal[2]))
    elif goal[4] and not goal[2] and not subs:
        print("| {}   ...".format(goal[1].upper()))
    else:
        print("| {}".format(goal[1].upper()))

    print("        {}{}{}{}{}".format(FONT_DICT['green no u'], '+' * percent_done,
            FONT_DICT['red no u'], '-' * (20 - percent_done), FONT_DICT['end']))
    # Check for Subtasks
    if goal[4] and subs:
        print_sub(int(goal[0] - 1), goal_data)


def view_goals(show_subs=False):
    """Displays all goals"""
    print()
    print('  ' + FONT_DICT['magenta'] + "GOALS" + FONT_DICT['end'], end='\n\n')
    if not goal_data:
        print("    No Goals Found")
        return
    for goal in goal_data:
        view_goal(int(goal[0]) - 1, show_subs)

    if show_subs:
        print(end='\n')
    else:
        print()
        print("        Subgoals Are Hidden. Use 'ls gs' To View Them", end='\n\n')


def auto_percentage(goal_num):
    """Calculate percentage completion from percentage of subgoals completed."""
    num_subs = len(goal_data[goal_num][4])
    if num_subs == 0:
        return 0

    done_subs = 0
    for sub in goal_data[goal_num][4]:
        if sub.endswith('^'):
            done_subs += 1
    return int((done_subs / num_subs) * 100)


def view_tag(command_extra):
    """Displays all Goals and Tasks with a specified tag."""
    tag_regex = re.search(r'^(\w*)\s?(\w*)?', command_extra)
    print(command_extra)
    tag = tag_regex.group(2).lower()
    print(tag)
    if not tag:
        tag = input("  Enter the Tag You Wish to View: ").lower()
    print()
    print('  ' + FONT_DICT['magenta'] + "GOALS TAGGED WITH "
          + tag.upper() + FONT_DICT['end'])
    for goal in goal_data:
        if tag in goal[5]:
            print("    {}| {} ({})".format(goal[0], goal[1], goal[2]))
    print()

    print('  ' + FONT_DICT['green'] + "TASKS TAGGED WITH "
          + tag.upper() + FONT_DICT['end'])
    for task in task_data:
        if tag in task[5]:
            print("    {}| {} ({})".format(task[0], task[1], task[2]))
    print()


def add_task(command_extra):
    """Adds system argument task to the task list."""
    add_regex = re.search(r'^"(.*)"\s?(\S*)?\s?(.*)?', command_extra)
    task = add_regex.group(1)
    opt_date = add_regex.group(2)
    opt_repeat = add_regex.group(3)

    if opt_date:
        if opt_date == 'tm':
            date_tomorrow = dt.strptime(current_date, '%Y-%m-%d') + timedelta(1)
            date = dt.strftime(date_tomorrow, '%Y-%m-%d')
        elif verify_date(opt_date):
            date = opt_date
        else:
            return
    else:
        date = current_date

    if opt_repeat:
        if verify_repeats(opt_repeat):
            repeat = parse_repeat(opt_repeat)
        else:
            return
    else:
        repeat = ''
    task_data.append([len(task_data) + 1, task, date, repeat, '', ''])


def add_goal(command_extra):
    """Adds a goal to the goal list."""
    gadd_regex = re.search(r'^"(.*)"\s?"?([^"]*)?"?\s?(.*)?', command_extra)
    goal = gadd_regex.group(1)
    opt_target = gadd_regex.group(2)
    opt_percent = gadd_regex.group(3)

    if opt_target:
        target = opt_target
    else:
        target = ''

    if opt_percent:
        percent = int(opt_percent)
    else:
        percent = 'auto'

    goal_data.append([len(goal_data) + 1, goal, target, percent, '', ''])


def delete_item(item_num, cache_list):
    """Removes an item from the task or goal list."""
    if cache_list is deleted_tasks:
        data_list = task_data
        undo_com = "'undo' or 'u'"
    elif cache_list is deleted_goals:
        data_list = goal_data
        undo_com = "'undo-goal' or 'ug'"
    cache_list.append(data_list.pop(item_num))
    print("  Item deleted. Enter {} to restore.".format(undo_com))


def complete_task(task_num):
    """Marks a task as complete."""
    repeat = task_data[task_num][3]
    if repeat != '':
        # Append copy of data so non-repeat date can be restored using 'Uncheck'
        data_copy = task_data[task_num][:]
        completed_tasks.append(data_copy)

        if type(repeat) is list:
            comp_list_rep(task_num, repeat)
            return

        old_date = dt.strptime(task_data[task_num][2], '%Y-%m-%d')
        new_date = old_date + timedelta(int(task_data[task_num][3]))
        task_data[task_num][2] = dt.strftime(new_date, '%Y-%m-%d')

        # Need to remove [Done] from completed subtasks
        if task_data[task_num][4] != '':
            reset_subs(task_num)
    else:
        completed_tasks.append(task_data.pop(task_num))
    print("  Task marked as complete. Enter 'uncheck' or 'uc' to restore.")


def complete_today():
    """Mark all of today's tasks as complete."""
    to_complete = []
    for task in task_data:
        if task[2] == current_date:
            to_complete.append(task[0] - 1)
    # Process tasks to be deleted in reverse to keep the task numbers the same
    for task_num in to_complete[::-1]:
        complete_task(task_num)


def comp_list_rep(task_num, repeat):
    """Calculates the next day due in the repeat list and changes the due date."""
    # Processing of date list repeat
    if '-' in repeat[0]:
        try:
            date_position = repeat.index(task_data[task_num][2])

        except ValueError:
            print("  Is The Due Date One of the Listed Repeat Dates? If Not, "
              "Change It To One.")
            return

        if date_position == len(repeat) - 1:
            print("  Reached The End of This Task's Repeat Dates So Marking as Complete.")
            completed_tasks.append(task_data.pop(task_num))
            print("  Task Marked as Complete. Enter 'uncheck' or 'uc' to Restore.")

        else:
            task_data[task_num][2] = repeat[date_position + 1]

            if task_data[task_num][4] != '':
                reset_subs(task_num)
            print("  Task Marked as Complete. Enter 'uncheck' or 'uc' to Restore.")
        return

    # Find the name of current due day for processing day name list
    current_due = dt.strptime(task_data[task_num][2], '%Y-%m-%d')
    current_day = dt.strftime(current_due, '%a').lower()
    # Find the next day listed
    try:
        day_position = repeat.index(current_day)
    except ValueError:
        print("  Is The Due Date One of the Listed Repeat Days? If Not, "
              "Change It To One.")
        return

    if day_position == len(repeat) - 1:
        target_day = repeat[0]
    else:
        target_day = repeat[day_position + 1]
    # Cycle through days until the day matches
    checked_day = current_due
    while True:
        day_test = checked_day + timedelta(1)
        day_name = dt.strftime(day_test, '%a').lower()
        if day_name == target_day:
            new_date = day_test
            break
        else:
            checked_day = day_test

    task_data[task_num][2] = dt.strftime(new_date, '%Y-%m-%d')

    if task_data[task_num][4] != '':
        reset_subs(task_num)

    print("  Task Marked as Complete. Enter 'uncheck' or 'uc' to Restore.")


def complete_goal(task_num):
    """Moves a goal to the completed cache."""
    completed_goals.append(goal_data.pop(task_num))
    print("  Goal marked as complete. Enter 'uncheck-goal' or 'ucg' to restore.")


def move_item(command_extra, data_list):
    """Change a goals position in the list."""
    move_regex = re.search(r'^(\d*)\s?(\d*)?', command_extra)
    item_num = int(move_regex.group(1)) - 1
    if move_regex.group(2):
        new_position = int(move_regex.group(2)) - 1
    else:
        print("  Moving '{}'".format(data_list[item_num][1]))
        new_position = int(input("  Enter the item's new position: ")) - 1

    data_list.insert(new_position, data_list.pop(item_num))


def move_sub(command_extra, data_list):
    """Change a subitem's position in the list."""
    moves_regex = re.search(r'^(\d*)\s(\d*)\s?(\d*)?', command_extra)
    item_num = int(moves_regex.group(1)) - 1
    subitem_num = int(moves_regex.group(2)) - 1
    if moves_regex.group(3):
        new_position = int(moves_regex.group(3)) - 1
    else:
        print("  Moving '{}'".format(data_list[item_num][4][subitem_num]))
        new_position = int(input("  Enter the item's new position: ")) - 1

    data_list[item_num][4].insert(new_position, data_list[item_num][4].pop(subitem_num))


def reset_subs(task_num):
    """Resets subtasks to non-completed status"""
    for num, subtask in enumerate(task_data[task_num][4]):
            task_data[task_num][4][num] = subtask.rstrip('^')


def edit_desc(command_extra, data_list):
    """Updates a task's description."""
    edit_regex = re.search(r'^(\w*)\s?(.*)?', command_extra)
    item_num = int(edit_regex.group(1)) - 1

    if edit_regex.group(2):
        data_list[item_num][1] = edit_regex.group(2)
    else:
        print("  Editing: '{}'".format(data_list[item_num][1]))
        print("  Enter the new description below:")
        new_desc = input("  ")
        data_list[item_num][1] = new_desc


def undo_action(cache_list):
    """Restores the last deleted or completed task to the task list."""
    if cache_list is completed_tasks or cache_list is deleted_tasks:
        data_list = task_data
    elif cache_list is completed_goals or cache_list is deleted_goals:
        data_list = goal_data

    # Check for a repeat flag. If found delete matching task before restoring
    if cache_list == completed_tasks and completed_tasks[-1][3] != '':
        description = completed_tasks[-1][1]
        for task in task_data:
            if description == task[1]:
                del task_data[int(task[0]) - 1]
                break
    data_list.append(cache_list.pop(-1))


def change_date(command_extra):
    """Changes the due date of a task."""
    date_regex = re.search(r'^(\w*)\s?(.*)?', command_extra)
    task_num = int(date_regex.group(1)) - 1
    command_date = date_regex.group(2)
    if command_date:
        if command_date == 't':
            task_data[task_num][2] = current_date
        elif command_date == 'tm':
            new_date = dt.strptime(current_date, '%Y-%m-%d') + timedelta(1)
            task_data[task_num][2] = dt.strftime(new_date, '%Y-%m-%d')
        else:
            if verify_date(date_regex.group(2)):
                task_data[task_num][2]
    else:
        print("  Enter New Due Date For {}: (YYYY-MM-DD)".format(task_data[task_num][1]))
        new_date = input("  ")
        if verify_date(new_date):
            task_data[task_num][2] = new_date


def add_repeat(command_extra):
    """Flags a task with the repeat flag so it auto-renews on completion."""
    repeat_regex = re.search(r'^(\w*)\s?(.*)?', command_extra)
    command_rep = repeat_regex.group(2)
    if command_rep:
        parsed_repeat = parse_repeat(command_rep)
        if verify_repeats(parsed_repeat):
            repeat = parsed_repeat

    else:
        print("  Enter Your Repeat e.g. '4' or 'tue or "
              "mon,wed,sat' or '2018-01-01,2018-02-01': ")
        inputted_repeat = input("  ").lower()
        parsed_repeat = parse_repeat(inputted_repeat)
        if verify_repeats(parsed_repeat):
            repeat = parsed_repeat

    task_data[int(repeat_regex.group(1)) - 1][3] = repeat
    print("  Repeat Sucessfully Added to Task.")


def parse_repeat(unparsed_rep):
    """Parses the repeat returning it as a single item or a list as appropriate."""
    if ',' in unparsed_rep:
            repeat = unparsed_rep.split(',')
    else:
            repeat = unparsed_rep
    return repeat


def change_target(command_extra):
    """Changes the target date of a goal."""
    target_regex = re.search(r'^(\w*)\s?(.*)?', command_extra)
    goal_num = int(target_regex.group(1)) - 1
    if target_regex.group(2):
        new_target = target_regex.group(2)
    else:
        print("  Enter New Target For {}:".format(goal_data[goal_num][1]))
        new_target = input("  ")
    goal_data[goal_num][2] = new_target


def change_percentage(command_extra):
    """Changes the completion percentage of a goal."""
    percentage_regex = re.search(r'^(\w*)\s?(.*)?', command_extra)
    goal_num = int(percentage_regex.group(1)) - 1
    if percentage_regex.group(2):
        new_percentage = percentage_regex.group(2)
    else:
        print("  Enter New Completion Percentage {}:".format(goal_data[goal_num][1]))
        new_percentage = input("  ")

    goal_data[goal_num][3] = new_percentage


def remove_value(data_list, task_num, value_position):
    """Removes a value from an item."""
    data_list[task_num][value_position] = ''


def update_order():
    """Updates the numbering of the tasks and goals."""
    task_data.sort(key=lambda x: x[2])
    count = 1
    for task in task_data:
        task[0] = count
        count += 1

    for num, goal in enumerate(goal_data, 1):
        goal[0] = num


def add_sub(command_extra, data_list):
    """Adds subtask to a task or goal."""
    sub_regex = re.search(r'^(\w*)\s?(.*)?', command_extra)
    item_num = int(sub_regex.group(1)) - 1
    subtask = sub_regex.group(2)
    if not subtask:
        print("  Enter Subitem:")
        subtask = input("  ")
    if data_list[item_num][4] == '':
        data_list[item_num][4] = [subtask]
    else:
        data_list[item_num][4].append(subtask)


def complete_sub(command_extra, data_list):
    """Marks a subtask as complete."""
    subcom_regex = re.search(r'^(\w*)\s?(.*)?', command_extra)
    item_num = int(subcom_regex.group(1)) - 1
    if subcom_regex.group(2):
        sub_num = int(subcom_regex.group(2)) - 1
    else:
        sub_num = int(input("  Enter the number of the subitem")) - 1
    data_list[item_num][4][sub_num] = data_list[item_num][4][sub_num] + '^'

    subs_done = True
    for subitem in data_list[item_num][4]:
        if not subitem.endswith('^'):
            subs_done = False
    if subs_done:
        print()
        item_decision = input("  All Subitems Are Complete, Would You Like to "
                              "Mark the Item as Complete (y/n): ")
        if item_decision.lower() == 'y':
            if data_list is task_data:
                complete_task(item_num)
            elif data_list is goal_data:
                complete_goal(item_num)


def uncomplete_sub(command_extra, data_list):
    """Unmarks a subtask as complete."""
    subuncom_regex = re.search(r'^(\w*)\s?(.*)?', command_extra)
    item_num = int(subuncom_regex.group(1)) - 1
    if subuncom_regex.group(2):
        sub_num = int(subuncom_regex.group(2)) - 1
    else:
        sub_num = int(input("  Enter the number of the subitem")) - 1
    data_list[item_num][4][sub_num] = data_list[item_num][4][sub_num].rstrip('^')


def delete_sub(command_extra, data_list):
    """Removes a subtask."""
    delcom_regex = re.search(r'^(\w*)\s?(.*)?', command_extra)
    item_num = int(delcom_regex.group(1)) - 1
    if delcom_regex.group(2):
        sub_num = int(delcom_regex.group(2)) - 1
    else:
        sub_num = input("  Enter the number of the subitem")
    del data_list[item_num][4][sub_num]


def edit_sub(command_extra, data_list):
    """Updates a subtask's description."""
    edits_regex = re.search(r'^(\d*)\s(\d*)\s?(.*)?', command_extra)
    item_num = int(edits_regex.group(1)) - 1
    sub_num = int(edits_regex.group(2)) - 1
    print("  Editing: '{}'".format(data_list[item_num][4][sub_num]))
    if edits_regex.group(3):
        data_list[item_num][4][sub_num] = edits_regex.group(3)
    else:
        print("  Enter the new subitem description below:")
        new_desc = input("  ")
        data_list[item_num][4][sub_num] = new_desc


def print_sub(item_num, data_list):
    """Prints a tasks subtasks."""
    for num, subtask in enumerate(data_list[item_num][4], 1):
        if subtask.endswith('^'):
            undone = subtask.rstrip('^')
            subtask = strike_text(undone)
        print("        {}".format(num).rjust(8) + ") {}".format(subtask))
    print()


def strike_text(text):
    """Adds a strikethtough effect to text."""
    striked = ''
    for char in text:
        striked = striked + char + '\u0336'
    return striked


def change_tag(command_extra, data_list):
    """Updates the tag(s) of a Task or Goal."""
    tag_regex = re.search(r'^(\d*)\s?(.*)?', command_extra)
    item_num = int(tag_regex.group(1)) - 1
    command_tag = tag_regex.group(2)
    if command_tag:
        tag = command_tag.lower().split(',')
    else:
        print("  Enter your tag(s) here. If multiple, seperate them with a comma:")
        tag = input("  ").lower().split(',')

    data_list[item_num][5] = tag


def save_changes():
    """Writes changes to file."""
    with open ('data.pickle', 'wb') as fp:
        pickle.dump(task_data, fp)
        pickle.dump(goal_data, fp)


def smart_display(mini=False):
    """Checks if list has tasks before dispaying it."""
    if not task_data:
        print()
        print(FONT_DICT['red no u'] + "    NO TASKS TO DISPLAY" + FONT_DICT['end'])
        return
    empty = True
    if task_data[0][2] < current_date:
        view_overdue()
        empty = False
    for task in task_data:
        if task[2] == current_date:
            view_today()
            empty = False
            break
    if mini:
        if empty:
            print()
            print(FONT_DICT['green no u'] + "    NO TASKS OVERDUE OR DUE TODAY"
                  + FONT_DICT['end'], end='\n\n')
        return

    for task in task_data:
        if ((dt.strptime(task[2], '%Y-%m-%d')
            - dt.strptime(current_date, '%Y-%m-%d')).days) == 1:
            view_tomorrow()
            break
    if ((dt.strptime(task_data[-1][2], '%Y-%m-%d')
        - dt.strptime(current_date, '%Y-%m-%d')).days) > 1:
        view_future()


def show_help():
    """Prints Taskian usage instructions to the screen."""
    print()
    with open('help.txt') as f:
        for line in f.readlines():
            print(line, end='')


def verify_date(potential_date):
    """Checks that a date is able to be parsed correctly."""
    try:
        dt.strptime(potential_date, '%Y-%m-%d')
    except ValueError:
        print("  Date Entered Doesn't Match the Required "
                   "(YYYY-MM-DD) Format.", end='\n\n')
        return False
    return True


def verify_repeats(parsed_repeat):
    """Check that a repeat is able to be parsed correctly."""
    if type(parsed_repeat) is list:
        if '-' in parsed_repeat[0]:
            for date in parsed_repeat:
                if not verify_date(date):
                    print("  ")
                    return False
        else:
            for day_name in parsed_repeat:
                if day_name not in DAY_NAMES:
                    print("  Not All Day Names Were In the Correct "
                            "Three Letter Format.", end='\n\n')
                    return False

    else:
        if '-' in parsed_repeat:
            if not verify_date(parsed_repeat):
                return
        elif parsed_repeat.isalpha():
            if not parsed_repeat in DAY_NAMES:
                print("  The Repeat Day Didn't Match "
                        "The Accepted Values.", end='\n\n')
                return False
    return True


# A dictionary of ANSI escapse sequences for font effects.
FONT_DICT = {
   'blue':  '\033[4;94m',
   'green':  '\033[4;92m',
   'green no u':  '\033[1;92m',
   'orange': '\033[4;93m',
   'red':  '\033[4;91m',
   'red no u':  '\033[1;91m',
   'magenta':  '\033[4;95m',
   'end':  '\033[0m',
}

# List of three-letter day names used to check repeat input
DAY_NAMES = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

with open('data.pickle', 'rb') as fp:
    task_data = pickle.load(fp)
    goal_data = pickle.load(fp)

# Cache Lists
deleted_tasks = []
completed_tasks = []
deleted_goals = []
completed_goals = []

current_date = dt.now().strftime('%Y-%m-%d')

# Initial display
if goal_data:
    view_goals()
smart_display(mini=True)

while True:
    action = input("  ENTER COMMAND ('q' to quit): ")
    print()
    if action.lower() == "q":
        break
    else:
        try:
            auto_display = decide_action(action)
        except IndexError:
            print()
            print("  No Item Found at That Position in the List or Cache - "
                  "Try Again or Enter 'h' for Usage Instructions.")
        except ValueError:
            print()
            print("  Did You Forget A Number For The Item/Subitem in Your Command? - "
                  "Try Again or Enter 'h' for Usage Instructions.")

        update_order()
        save_changes()
        if auto_display:
            smart_display()