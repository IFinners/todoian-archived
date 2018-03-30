#!/usr/bin/env python3

class Task:
    """Class for all tasks."""

    def __init__(self, num, task, due_date='', additional_info=''):
        """Initialise the Task class."""
        self.num = num
        self.task = task
        self.due_date = due_date
        self.additional_info = additional_info

    def set_date(self, date):
        """Sets the due date for the task."""
        self.due_date = date

    def set_additional(self, info_string):
        """Sets additional information about the task."""
        self.additional_info = info_string

    def display_additional(self):
        """Displays a tasks additional information."""
        print("Additional Information for '" + self.task + "':")
        print()
        print(self.additional_info)