import tkinter as tk
from gui import TaskGUI
from task_manager import TaskManager

if __name__ == "__main__":
    root = tk.Tk()
    task_manager = TaskManager()
    app = TaskGUI(root, task_manager)
    root.mainloop()
