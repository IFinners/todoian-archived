#!/usr/bin/env python3

"""Todo list."""

import sys
import datetime

from task_class import Task

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
            cache_task(deleted, int(to_remove) - 1)

    elif command.startswith('d '):
        to_complete = int(command[2:]) - 1
        cache_task(completed, int(to_complete))

    elif command == "undo" or command == "u":
        undo_action(deleted)
    
    elif command == "uncheck" or command == "uc":
        undo_action(completed)


def view_overdue():
    """Prints all overdue tasks to the terminal."""
    print()
    print("OVERDUE TASKS:")
    print()
    for task in task_data:
        if task[2] < current_date:
            print("{}: {} [{}]".format(task[0], task[1], task[2]))
    print()


def view_today():
    """Prints all of today's tasks to the terminal.."""
    print()
    print("TODAY'S TASKS:")
    print()
    for task in task_data:
        if task[2] == current_date:
            print("{}: {}".format(task[0], task[1]))
    print()


def view_future():
    """Prints all future tasks to the terminal.."""
    print()
    print("FUTURE TASKS:")
    print()
    for task in task_data:
        if task[2] > current_date:
            print("{}: {} [{}]".format(task[0], task[1], task[2]))
    print()


def add_task(task):
    """Adds system argument task to the task list."""
    Task(len(task_data) + 1, task, current_date)
    task_data.append([len(task_data) + 1, task, current_date, ''])


def cache_task(cache_list, task_num):
    """Removes a task from the task list."""
    if cache_list == deleted:
        fate = "deleted"
        undo_com = "'undo' or 'u'"
    elif cache_list == completed:
        fate = "completed"
        undo_com = "'uncheck' or 'uc'"
    cache_list.append(task_data.pop(task_num))
    print("Task {}. Enter {} as your command to "
          "restore this item".format(fate, undo_com))
              

def undo_action(action):
    """Restores the last deleted or completed task to the task list."""
    task_data.insert(int(action[-1][0]), action.pop(-1))


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
    Task(num, task[0], task[1], task[2])
temp_data.clear()

deleted = []
completed = []

current_date = datetime.datetime.now().strftime('%Y-%m-%d')

view_overdue()
view_today()

while True:
    action = input("Enter you command here (or enter 'q' to quit): ")
    if action.lower() == "q":
        break
    else:
        decide_action(action)

with open('tasks.txt', mode='w') as f:
    for task_info in task_data:
        f.write("{}|{}|{}\n".format(task_info[1], task_info[2], task_info[3]))
