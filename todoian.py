#!/usr/bin/env python3

"""Todo list."""

import sys

def decide_action(command):
    """Decides which action the argument requires."""
    if command.lower() == "list" or command.lower() == "ls":
        list_tasks()
    
    elif command.startswith('a '):
        task = command[2:]
        add_task(task)
    
    elif command.startswith('rm '):
        to_remove = command[3:]
        if to_remove == "all":
            tasks.clear()
        else:
            delete_task(int(to_remove) - 1)

    elif command.startswith('d '):
        task_num = int(command[2:]) - 1
        complete_task(task_num)

    elif command.startswith('mv'):
        numbers = command[3:].split(' ')
        move_task(int(numbers[0]), int(numbers[1]))
    
    elif command == "undo" or command == "u":
        undo_action(deleted)
    
    elif command == "uncheck" or command == "uc":
        undo_action(completed)


def list_tasks():
    """Prints all current tasks to the console."""
    print()
    print("TODO:")
    print()
    for num, task in enumerate(tasks, 1):
        print(str(num) + ": " + task)
    print()


def add_task(task):
    """Adds system argument task to the task list."""
    tasks.append(task)


def delete_task(task_num):
    """Removes a task from the task list."""
    deleted.append(task_num)
    deleted.append(tasks.pop(task_num))
    print("Task deleted. Enter 'undo' as your command to "
            "restore this item to the list.")


def complete_task(task_num):
    """Moves a task to the completed list."""
    completed.append(task_num)
    completed.append(tasks.pop(task_num))
    print("Task marked as completed. Enter 'uncheck' as your command to "
            "restore this item to the list.")
              

def undo_action(action):
    """Restores the last deleted or completed task to the task list."""
    tasks.insert(int(action[-2]), action.pop(-1))
    del action[-1]


def move_task(to_move, move_to):
    """Move a task to a new position in the todo list."""
    tasks.insert(int(move_to) - 1, tasks.pop(int(to_move) - 1))


with open('tasks.txt') as f:
    tasks = f.read().splitlines()
    
deleted = []
completed = []

list_tasks()
print()
while True:
    action = input("Enter you command here (or enter 'q' to quit): ")
    if action.lower() == "q":
        break
    else:
        decide_action(action)

with open('tasks.txt', mode='w') as f:
    for task in tasks:
        f.write(task + '\n')
