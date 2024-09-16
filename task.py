from datetime import datetime

class Task:
    def __init__(self, title, description, priority):
        self.title = title
        self.description = description
        self._priority = priority  # Protected attribute
        self._completed = False  # Task completion status

    def mark_as_completed(self):
        self._completed = True

    def is_completed(self):
        return self._completed

    def get_priority(self):
        return self._priority

    def __str__(self):
        return f'{self.title} ({self._priority}) - {"Completed" if self._completed else "Pending"}'

class WorkTask(Task):
    def __init__(self, title, description, priority, deadline):
        super().__init__(title, description, priority)
        self.__deadline = deadline  # Private attribute

    def set_deadline(self, deadline):
        self.__deadline = deadline

    def get_deadline(self):
        return self.__deadline

    def __str__(self):
        return f'{super().__str__()} - Deadline: {self.__deadline}'

class HomeTask(Task):
    def __init__(self, title, description, priority):
        super().__init__(title, description, priority)

class HealthTask(Task):
    def __init__(self, title, description, priority, routine):
        super().__init__(title, description, priority)
        self.routine = routine

    def __str__(self):
        return f'{super().__str__()} - Routine: {self.routine}'
