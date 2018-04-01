#!/usr/bin/env python3

"""Todo list."""

import re
from datetime import datetime as dt
from datetime import timedelta


def decide_action(command):
    """Decides which action the argument requires."""
    command_regex = re.search(r'^(\w*)\s?(.*)', command)
    
    if command_regex.group(1).lower() in ('ls','list'):
        if command_regex.group(2).lower() in ('t', 'today'):
            view_today()
        elif command_regex.group(2).lower() in ('o', 'overdue'):
            view_overdue()
        elif command_regex.group(2).lower() in ('f', 'future'):
            view_future()
        elif command_regex.group(2).lower() in ('a', 'all'):
            view_overdue()
            view_today()
            view_future()
        else:
            smart_display()
    
    elif command_regex.group(1).lower() in ('a', 'add'):
        add_task(command_regex.group(2))
    
    elif command_regex.group(1).lower() in ('rm', 'remove'):
        if command_regex.group(2).lower() in ("all", 'a'):
            task_data.clear()
        else:
            delete_task(int(command_regex.group(2)) - 1)

    elif command_regex.group(1).lower() in ('c', 'complete', 'comp'):
        complete_task(int(command_regex.group(2)) - 1)

    elif command_regex.group(1).lower() in ('e', 'ed', 'edit'):
        edit_desc(command_regex.group(2))
    
    elif command_regex.group(1).lower() in ('cd', 'change date'):
        change_date(command_regex.group(2))
    
    elif command_regex.group(1).lower() in ('ar', 'add repeat'):
        add_repeat(command_regex.group(2))

    elif command_regex.group(1).lower() in ('rr', 'remove repeat'):
        remove_repeat(int(command_regex.group(2)) - 1)

    elif command_regex.group(1).lower() in ('s', 'sub', 'subtask'):
        add_sub(command_regex.group(2))

    elif command_regex.group(1).lower() in ('cs', 'comp subtask'):
        complete_sub(command_regex.group(2))

    elif command_regex.group(1).lower() in ('rs', 'rm sub', 'remove subtask'):
        delete_sub(command_regex.group(2))
        
    elif command.lower() in ('u', 'undo'):
        undo_action(deleted_cache)
    
    elif command.lower() in ('uc', 'uncheck'):
        undo_action(completed_cache)
    
    elif command_regex.group(1).lower() == 'save':
        save_changes()


def view_today():
    """Prints all of today's tasks to the terminal.."""
    print()
    print('  ' + font_dict['green'] + font_dict['under'] + "TODAY'S TASKS"
          + font_dict['end'])
    empty = True
    for task in task_data:
        if task[2] == current_date:
            print("    {}| {}".format(task[0], task[1]))
            # Check for Subtasks
            if task[4]:
                print_sub(int(task[0] - 1))
            empty = False
    if empty:
        print("    No Tasks Found")
    print()


def view_overdue():
    """Prints all overdue tasks to the terminal."""
    print()
    print('  ' + font_dict['red'] + font_dict['under'] + "OVERDUE TASKS"
          + font_dict['end'])
    empty = True
    for task in task_data:
        if task[2] < current_date:
            over = ((dt.strptime(current_date, '%Y-%m-%d')
                          - dt.strptime(task[2], '%Y-%m-%d')).days)
            if over == 1:
                print("    {}| {} [Due Yesterday]".format(task[0], task[1]))
            else:
                print("    {}| {} [Due {} Days Ago]".format(task[0], task[1], over))
            # Check for Subtasks
            if task[4]:
                print_sub(int(task[0] - 1))
            empty = False
    if empty:
        print("    No Tasks Found")
    print()


def view_future():
    """Prints all future tasks to the terminal.."""
    print()
    print('  ' + font_dict['blue'] + font_dict['under'] + "FUTURE TASKS"
          + font_dict['end'])
    empty = True
    for task in task_data:
        if task[2] > current_date:
            until = ((dt.strptime(task[2], '%Y-%m-%d')
                          - dt.strptime(current_date, '%Y-%m-%d')).days)
            if until == 1:
                print("    {}| {} [Due Tommorow]".format(task[0], task[1]))
            else:
                print("    {}| {} [Due in {} Days]".format(task[0], task[1], until))
            # Check for Subtasks
            if task[4]:
                print_sub(int(task[0] - 1))
            empty = False
    if empty:
        print("    No Tasks Found")
    print()


def add_task(command_extra):
    """Adds system argument task to the task list."""
    add_regex = re.search(r'^"(.*)"\s?(\S*)?\s?(\w)?', command_extra)
    task = add_regex.group(1)
    if add_regex.group(2):
        date = add_regex.group(2)
    else:
        date = current_date
    if add_regex.group(3):
        repeat = int(add_regex.group(3))
    else:
        repeat = ''
    task_data.append([len(task_data) + 1, task, date, repeat, ''])
    update_order()


def delete_task(task_num):
    """Removes a task from the task list."""
    deleted_cache.append(task_data.pop(task_num))
    update_order()
    print("  Task deleted. Enter 'undo' or 'u' to restore.")

def complete_task(task_num):
    """Marks a task as complete."""
    if task_data[task_num][3] != '':
        old_date = dt.strptime(task_data[task_num][2], '%Y-%m-%d')
        new_date = old_date + timedelta(int(task_data[task_num][3]))
        task_data[task_num][2] = dt.strftime(new_date, '%Y-%m-%d')
        # Need to remove [Done] from completed subtasks
        if task_data[task_num][4] != '':
            print("subs found!")
            for num, subtask in enumerate(task_data[task_num][4]):
                task_data[task_num][4][num] = subtask.rstrip('[Done]')

    else:
        completed_cache.append(task_data.pop(task_num))
    print("  Task marked as complete. Enter 'uncheck' or 'uc' to restore.")
    update_order()


def edit_desc(command_extra):
    """Updates a task's description."""
    edit_regex = re.search(r'^(\w)\s?(.*)?', command_extra)
    task_num = int(edit_regex.group(1)) - 1
    print("  Editing: '{}'".format(task_data[task_num][1]))
    if edit_regex.group(2):
        task_data[task_num][1] = edit_regex.group(2)
    else:
        print("  Enter the new task description below:")
        new_desc = input("  ")
        task_data[task_num][1] = new_desc


def undo_action(action):
    """Restores the last deleted or completed task to the task list."""
    task_data.append(action.pop(-1))
    update_order()

def change_date(command_extra):
    """Changes the due date of a task."""
    date_regex = re.search(r'^(\w)\s?(.*)?', command_extra)
    task_num = int(date_regex.group(1)) - 1
    if date_regex.group(2):
        if date_regex.group(2) == 't':
            task_data[task_num][2] = current_date
        else:
            task_data[task_num][2] = date_regex.group(2)
    else:
        print("  Enter new due_date for {}: (YYYY-MM-DD)")
        new_date = input("  ")
        task_data[task_num][2] = new_date
        update_order()


def add_repeat(command_extra):
    """Flags a task with the repeat flag so it auto-renews on completion."""
    repeat_regex = re.search(r'^(\w)\s?(.*)?', command_extra)
    if repeat_regex.group(2):
        step = repeat_regex.group(2)
    else:
        step = input("  Enter how many days until the task should repeat: ")
    task_data[int(repeat_regex.group(1)) - 1][3] = step


def remove_repeat(task_num):
    """Removes the repeat flag from a task."""
    task_data[task_num][3] = ''


def update_order():
    """Updates the numbering of the tasks."""
    task_data.sort(key=lambda x: x[2])
    count = 1
    for task in task_data:
        task[0] = count
        count += 1


def add_sub(command_extra):
    """Adds subtask to a task."""
    sub_regex = re.search(r'^(\w)\s?(.*)?', command_extra)
    task_num = int(sub_regex.group(1)) - 1
    subtask = sub_regex.group(2)
    if not subtask:
        print("Enter Subtask:")
        subtask = input()
    if task_data[task_num][4] == '':
        task_data[task_num][4] = [subtask]
    else:
        task_data[task_num][4].append(subtask)


def complete_sub(command_extra):
    """Marks a subtask as complete."""
    subcom_regex = re.search(r'^(\w)\s?(.*)?', command_extra)
    task_num = int(subcom_regex.group(1)) - 1
    if subcom_regex.group(2):
        sub_num = int(subcom_regex.group(2)) - 1
    else:
        sub_num = int(input("  Enter the number of the subtask")) - 1
    task_data[task_num][4][sub_num] = task_data[task_num][4][sub_num] + " [Done]" 


def delete_sub(command_extra):
    """Removes a subtask."""
    delcom_regex = re.search(r'^(\w)\s?(.*)?', command_extra)
    task_num = int(delcom_regex.group(1)) - 1
    if delcom_regex.group(2):
        sub_num = int(delcom_regex.group(2)) - 1
    else:
        sub_num = input("  Enter the number of the subtask")
    del task_data[task_num][4][sub_num]


def print_sub(task_num):
    """Prints a tasks subtasks."""
    for subtask in task_data[task_num][4]:
        if subtask[-6:] == '[Done]':
            undone = subtask.rstrip('[Done]')
            subtask = strike_text(undone)
        print("        +) {}".format(subtask))
    print()


def strike_text(text):
    """Adds a strikethtough effect to text."""
    striked = ''
    for char in text:
        striked = striked + char + '\u0336'
    return striked


def save_changes():
    """Writes changes to file."""
    with open('tasks.txt', mode='w') as f:
        for task_info in task_data:
            f.write("{}|+|{}|+|{}|+|{}\n".format(task_info[1], task_info[2],
                    task_info[3], '+|+'.join(task_info[4])))

def smart_display():
    """."""
    if task_data[0][2] < current_date:
        view_overdue()
    view_today()
    if task_data[-1][2] > current_date:
        view_future()


# A dictionary of ANSI escapse sequences for font effects.
font_dict = {
   'blue':  '\033[94m',
   'green':  '\033[92m',
   'red':  '\033[91m',
   'bold': '\033[1m',
   'under':  '\033[4m',
   'end':  '\033[0m',
}

with open('tasks.txt') as f:
    tasks_info = f.read().splitlines()

# Saved data parsing
task_data = []
for num, line in enumerate(tasks_info, 1):
    info = line.split('|+|')
    data_list = [num]
    data_list.append(info[0])
    data_list.append(info[1])
    data_list.append(info[2])
    # Subtask detection and parsing
    if info[3] != '':
        sub_list = info[3].split('+|+')
    else:
        sub_list = ''
    data_list.append(sub_list)
    task_data.append(data_list)
update_order()

deleted_cache = []
completed_cache = []

current_date = dt.now().strftime('%Y-%m-%d')

# Initial display
smart_display()
print('\n')

while True:
    action = input("  ENTER COMMAND ('q' to quit): ")
    if action.lower() == "q":
        break
    else:
        decide_action(action)
        print('\n')
        if 'ls' not in action:
            smart_display()

save_changes()
