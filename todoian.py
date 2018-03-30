#!/usr/bin/env python3

"""Todo list."""

import sys
import datetime

from task_class import Task

def decide_action(command):
    """Decides which action the argument requires."""
    if command.lower() == 'list' or command.lower() == 'ls':
        list_tasks()

    elif command.lower() == 'list all' or command.lower() == 'ls a':
        list_tasks(True)
    
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
        task_num = int(command[2:]) - 1
        cache_task(completed, task_num)

    elif command.startswith('mv'):
        numbers = command[3:].split(' ')
        move_task(int(numbers[0]), int(numbers[1]))
    
    elif command == "undo" or command == "u":
        undo_action(deleted)
    
    elif command == "uncheck" or command == "uc":
        undo_action(completed)


def list_tasks(view_all=None):
    """Printtasks to the console either overdue and today's or all."""
    print()
    print("OVERDUE TASKS:")
    print()
    for num, task in enumerate(task_data, 1):
        if task[1] < current_date:
            print("{}: {} [{}]".format(num, task[0], task[1]))
    print()
    
    print()
    print("TODAY's TASKS:")
    print()
    for num, task in enumerate(task_data, 1):
        if task[1] == current_date:
            print("{}: {}".format(num, task[0]))
    print()

    if view_all != None:
        print()
        print("FUTURE TASKS:")
        print()
        for num, task in enumerate(task_data, 1):
            if task[1] > current_date:
                print("{}: {} [{}]".format(num, task[0], task[1]))
        print()


def add_task(task):
    """Adds system argument task to the task list."""
    Task(task, current_date)
    task_data.append([task, current_date, ''])


def cache_task(cache_list, task_num):
    """Removes a task from the task list."""
    if cache_list == deleted:
        fate = "deleted"
        undo_com = "'undo' or 'u'"
    elif cache_list == completed:
        fate = "completed"
        undo_com = "'uncheck' or 'uc'"
    cache_list.append(task_num)
    cache_list.append(task_data.pop(task_num))
    print("Task {}. Enter {} as your command to "
          "restore this item".format(fate, undo_com))
              

def undo_action(action):
    """Restores the last deleted or completed task to the task list."""
    task_data.insert(int(action[-2]), action.pop(-1))
    del action[-1]


def move_task(to_move, move_to):
    """Move a task to a new position in the todo list."""
    task_data.insert(int(move_to) - 1, task_data.pop(int(to_move) - 1))


with open('tasks.txt') as f:
    tasks_info = f.read().splitlines()

task_data = []
for line in tasks_info:
    info = line.split('|')
    Task(info[0], [1], [2])
    task_data.append(info)
task_data.sort(key=lambda x: x[1])


deleted = []
completed = []

current_date = datetime.datetime.now().strftime('%Y-%m-%d')

list_tasks()
print()
while True:
    action = input("Enter you command here (or enter 'q' to quit): ")
    if action.lower() == "q":
        break
    else:
        decide_action(action)

with open('tasks.txt', mode='w') as f:
    for task_info in task_data:
        f.write('|'.join(task_info) + '\n')
