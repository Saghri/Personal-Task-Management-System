import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
from task_manager import TaskManager
from task import WorkTask, HomeTask, HealthTask


class TaskGUI:
    def __init__(self, root, task_manager):
        self.root = root
        self.root.title("Personal Task Management System")
        self.root.geometry("600x600")  # Enlarged Window
        self.task_manager = task_manager
        self.deadline = None  # Holds the selected deadline

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(self.root, text="Task Title")
        self.title_label.grid(row=0, column=0)

        # Title Entry
        self.title_entry = tk.Entry(self.root, width=30)
        self.title_entry.grid(row=0, column=1)

        # Description Label
        self.desc_label = tk.Label(self.root, text="Task Description")
        self.desc_label.grid(row=1, column=0)

        # Description Entry
        self.desc_entry = tk.Entry(self.root, width=30)
        self.desc_entry.grid(row=1, column=1)

        # Priority Label
        self.priority_label = tk.Label(self.root, text="Priority (Low/Medium/High)")
        self.priority_label.grid(row=2, column=0)

        # Priority Entry
        self.priority_entry = tk.Entry(self.root, width=30)
        self.priority_entry.grid(row=2, column=1)

        # Category Label
        self.category_label = tk.Label(self.root, text="Task Category (Work/Home/Health)")
        self.category_label.grid(row=3, column=0)

        # Category Entry
        self.category_entry = tk.Entry(self.root, width=30)
        self.category_entry.grid(row=3, column=1)

        # Calendar Button for Deadline
        self.calendar_button = tk.Button(self.root, text="Select Deadline", command=self.open_calendar)
        self.calendar_button.grid(row=4, column=1)

        # Add Task Button
        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.grid(row=5, column=1)

        # Display Tasks by Category
        self.category_buttons_frame = tk.Frame(self.root)
        self.category_buttons_frame.grid(row=6, column=0, columnspan=2)

        self.work_button = tk.Button(self.category_buttons_frame, text="View Work Tasks", command=self.view_work_tasks)
        self.work_button.pack(side=tk.LEFT, padx=10)  # Added padding between buttons

        self.home_button = tk.Button(self.category_buttons_frame, text="View Home Tasks", command=self.view_home_tasks)
        self.home_button.pack(side=tk.LEFT, padx=10)  # Added padding between buttons

        self.health_button = tk.Button(self.category_buttons_frame, text="View Health Tasks", command=self.view_health_tasks)
        self.health_button.pack(side=tk.LEFT, padx=10)  # Added padding between buttons

        # Scrollable Task List
        self.create_scrollable_task_list()

    def create_scrollable_task_list(self):
        # Scrollable frame for tasks
        self.scroll_canvas = tk.Canvas(self.root, width=550, height=200)
        self.scroll_canvas.grid(row=7, column=0, columnspan=2)

        self.scrollable_frame = tk.Frame(self.scroll_canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))

        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.scroll_canvas.yview)
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.grid(row=7, column=2, sticky="ns")
        self.scroll_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

    def open_calendar(self):
        # Open a new window for calendar selection
        self.calendar_window = tk.Toplevel(self.root)
        self.calendar_window.title("Select Deadline")
        self.calendar_window.geometry("300x300")

        today = datetime.today()

        # Calendar widget for selecting deadline, disabling past dates
        self.calendar = Calendar(self.calendar_window, selectmode='day', year=today.year, month=today.month, day=today.day, 
                                 mindate=today)
        self.calendar.pack(pady=20)

        # Confirm date button
        confirm_button = tk.Button(self.calendar_window, text="Confirm Date", command=self.confirm_date)
        confirm_button.pack(pady=10)

    def confirm_date(self):
        # Get the selected date from the calendar and set it as the deadline
        self.deadline = self.calendar.get_date()
        self.calendar_window.destroy()

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()
        priority = self.priority_entry.get()
        category = self.category_entry.get().lower()
        deadline = self.deadline  # Get the selected deadline

        if not title or not description or not priority or not category:
            messagebox.showwarning("Input Error", "All fields except Extra are required")
            return

        if category == "work":
            task = WorkTask(title, description, priority, deadline)
        elif category == "home":
            task = HomeTask(title, description, priority)
        elif category == "health":
            task = HealthTask(title, description, priority, deadline)
        else:
            messagebox.showwarning("Input Error", "Invalid category. Choose from Work, Home, or Health.")
            return

        self.task_manager.add_task(task)
        self.refresh_tasks()

    def refresh_tasks(self):
        # Clear previous tasks
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Sort tasks by priority: High = 1, Medium = 2, Low = 3
        priority_mapping = {"high": 1, "medium": 2, "low": 3}
        sorted_tasks = sorted(self.task_manager.get_pending_tasks(), key=lambda task: priority_mapping[task._priority.lower()])

        # Display tasks
        for task in sorted_tasks:
            task_label = tk.Label(self.scrollable_frame, text=str(task))
            task_label.pack()

    def view_work_tasks(self):
        self.display_category_tasks("work")

    def view_home_tasks(self):
        self.display_category_tasks("home")

    def view_health_tasks(self):
        self.display_category_tasks("health")

    def display_category_tasks(self, category):
        tasks = [task for task in self.task_manager.get_pending_tasks() if task.__class__.__name__.lower().startswith(category)]

        window = tk.Toplevel(self.root)
        window.title(f"{category.capitalize()} Tasks")
        window.geometry("400x400")

        for task in tasks:
            task_label = tk.Label(window, text=str(task))
            task_label.pack()

