#!/usr/bin/env python3

"""Todo list."""

import sys
from datetime import datetime
from datetime import timedelta


def decide_action(command):
    """Decides which action the argument requires."""
    if command.lower() == 'list' or command.lower() == 'ls':
        view_overdue()
        view_today()

    elif command.lower() == 'list today' or command.lower() == 'ls t':
        view_today()

    elif command.lower() == 'list overdue' or command.lower() == 'ls o':
        view_overdue()
    
    elif command.lower() == 'list future' or command.lower() == 'ls f':
        view_future()
    
    elif command.lower() == 'list all' or command.lower() == 'ls a':
        view_overdue()
        view_today()
        view_future()
    
    elif command.startswith('a '):
        task = command[2:]
        add_task(task)
    
    elif command.startswith('rm '):
        to_remove = command[3:]
        if to_remove == "all":
            task_data.clear()
        else:
            delete_task(int(to_remove) - 1)

    elif command.startswith('d '):
        to_complete = int(command[2:]) - 1
        complete_task(to_complete)

    elif command.startswith('cd '):
        to_change = int(command[3:]) - 1
        change_date(to_change)
    
    elif command.startswith('ar '):
        to_change = int(command[3:]) - 1
        add_repeat(to_change)

    elif command.startswith('rr '):
        to_change = int(command[3:]) - 1
        remove_repeat(to_change)

    elif command == "undo" or command == "u":
        undo_action(deleted)
    
    elif command == "uncheck" or command == "uc":
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
            over = ((datetime.strptime(current_date, '%Y-%m-%d')
                          - datetime.strptime(task[2], '%Y-%m-%d')).days)
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
            until = ((datetime.strptime(task[2], '%Y-%m-%d')
                          - datetime.strptime(current_date, '%Y-%m-%d')).days)
            if until == 1:
                print("{}: {} [Due Tommorow]".format(task[0], task[1]))
            else:
                print("{}: {} [Due in {} Days]".format(task[0], task[1], until))
    print()


def add_task(task):
    """Adds system argument task to the task list."""
    task_data.append([len(task_data) + 1, task, current_date, ''])


def delete_task(task_num):
    """Removes a task from the task list."""
    deleted.append(task_data.pop(task_num))
    print("Task deleted. Enter 'undo' or 'u' as a command to restore this item.")

def complete_task(task_num):
    """Marks a task as complete."""
    if task_data[task_num][3] != '':
        old_date = datetime.strptime(task_data[task_num][2], '%Y-%m-%d')
        new_date = old_date + timedelta(int(task_data[task_num][3]))
        task_data[task_num][2] = datetime.strftime(new_date, '%Y-%m-%d')
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

# Temp so it can be sorted by date and number used for creating class member.
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

current_date = datetime.now().strftime('%Y-%m-%d')
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
