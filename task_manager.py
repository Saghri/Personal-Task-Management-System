class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks

    def get_pending_tasks(self):
        return [task for task in self.tasks if not task.is_completed()]

    def get_completed_tasks(self):
        return [task for task in self.tasks if task.is_completed()]

    def sort_by_priority(self):
        self.tasks.sort(key=lambda task: task.get_priority())

    def mark_task_completed(self, task_title):
        for task in self.tasks:
            if task.title == task_title:
                task.mark_as_completed()
                return True
        return False
