#!/usr/bin/env python3

"""Todo list."""

import sys
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
            view_overdue()
            view_today()
    
    elif command_regex.group(1).lower() in ('a', 'add'):
        add_task(command_regex.group(2))
    
    elif command_regex.group(1).lower() in ('rm', 'remove', 'del'):
        if command_regex.group(2).lower() == "all":
            task_data.clear()
        else:
            delete_task(int(command_regex.group(2)) - 1)

    elif command_regex.group(1).lower() in ('d', 'done'):
        complete_task(int(command_regex.group(2)) - 1)

    elif command_regex.group(1).lower() == 'cd':
        change_date(int(command_regex.group(2)) - 1)
    
    elif command_regex.group(1).lower() == 'ar':
        add_repeat(int(command_regex.group(2)) - 1)

    elif command_regex.group(1).lower() == 'rr':
        remove_repeat(int(command_regex.group(2)) - 1)

    elif command.lower() in ('u', 'undo'):
        undo_action(deleted)
    
    elif command.lower() in ('uc', 'uncheck'):
        undo_action(completed)


def view_today():
    """Prints all of today's tasks to the terminal.."""
    print()
    print("TODAY'S TASKS:")
    print()
    for task in task_data:
        if task[2] == current_date:
            print("{}: {}".format(task[0], task[1]))
    print()


def view_overdue():
    """Prints all overdue tasks to the terminal."""
    print()
    print("OVERDUE TASKS:")
    print()
    for task in task_data:
        if task[2] < current_date:
            over = ((dt.strptime(current_date, '%Y-%m-%d')
                          - dt.strptime(task[2], '%Y-%m-%d')).days)
            if over == 1:
                print("{}: {} [Due Yesterday]".format(task[0], task[1]))
            else:
                print("{}: {} [Due {} Days Ago]".format(task[0], task[1], over))
    print()


def view_future():
    """Prints all future tasks to the terminal.."""
    print()
    print("FUTURE TASKS:")
    print()
    for task in task_data:
        if task[2] > current_date:
            until = ((dt.strptime(task[2], '%Y-%m-%d')
                          - dt.strptime(current_date, '%Y-%m-%d')).days)
            if until == 1:
                print("{}: {} [Due Tommorow]".format(task[0], task[1]))
            else:
                print("{}: {} [Due in {} Days]".format(task[0], task[1], until))
    print()


def add_task(task_details):
    """Adds system argument task to the task list."""
    add_regex = re.search(r'^"(.*)"\s?(\S*)?\s?(\w)?', task_details)
    task = add_regex.group(1)
    print(task)
    if add_regex.group(2):
        date = add_regex.group(2)
    else:
        date = current_date
    if add_regex.group(3):
        repeat = int(add_regex.group(3))
    else:
        repeat = ''
    task_data.append([len(task_data) + 1, task, date, repeat])


def delete_task(task_num):
    """Removes a task from the task list."""
    deleted.append(task_data.pop(task_num))
    print("Task deleted. Enter 'undo' or 'u' as a command to restore this item.")

def complete_task(task_num):
    """Marks a task as complete."""
    if task_data[task_num][3] != '':
        old_date = dt.strptime(task_data[task_num][2], '%Y-%m-%d')
        new_date = old_date + timedelta(int(task_data[task_num][3]))
        task_data[task_num][2] = dt.strftime(new_date, '%Y-%m-%d')
    else:
        completed.append(task_data.pop(task_num))

def undo_action(action):
    """Restores the last deleted or completed task to the task list."""
    task_data.insert(int(action[-1][0]), action.pop(-1))

def change_date(task_num):
    """Changes the due date of a task."""
    print("Enter new due_date for {}: (YYYY-MM-DD)")
    new_date = input()
    task_data[task_num][2] = new_date


def add_repeat(task_num):
    """Flags a task with the repeat flag so it auto-renews on completion."""
    step = input("How often would you like the task to be repeated (in days)? ")
    task_data[task_num][3] = step
    print(task_data[task_num][3])


def remove_repeat(task_num):
    """Removes the repeat flag from a task."""
    task_data[task_num][3] = ''


with open('tasks.txt') as f:
    tasks_info = f.read().splitlines()

# Temp so it can be sorted by date and number before being appended to list.
temp_data = []
for line in tasks_info:
    info = line.split('|')
    temp_data.append(info)

task_data = []
temp_data.sort(key=lambda x: x[1])
for num, task in enumerate(temp_data, 1):
    task_data.append([num, task[0], task[1], task[2]])
temp_data.clear()

deleted = []
completed = []

current_date = dt.now().strftime('%Y-%m-%d')
view_overdue()
view_today()

while True:
    action = input("Enter you command here (or enter 'q' to quit): ")
    if action.lower() == "q":
        break
    else:
        decide_action(action)
        print()

with open('tasks.txt', mode='w') as f:
    for task_info in task_data:
        f.write("{}|{}|{}\n".format(task_info[1], task_info[2], task_info[3]))
