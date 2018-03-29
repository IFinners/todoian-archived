#!/usr/bin/env python3

class Task:
    """Class for all tasks."""
    num_tasks = 0

    def __init__(self, name, due_date='', additional_info=''):
        """Initialise the Task class."""
        self.name = name
        self.due_date = due_date
        self.additional_info = additional_info
        Task.num_tasks += 1

    def set_date(self, date):
        """Sets the due date for the task."""
        self.due_date = date

    def set_additional(self, info_string):
        """Sets additional information about the task."""
        self.additional_info = info_string

    def display_additional(self):
        """Displays a tasks additional information."""
        print("Additional Information for '" + self.name + "':")
        print(self.additional_info)