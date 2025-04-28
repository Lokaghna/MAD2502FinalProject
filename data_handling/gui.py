import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import matplotlib.pyplot as plt
import numpy as np
from dataclass_models import Task
from functions_new import load_data, tasks

# reference for gui: https://www.geeksforgeeks.org/python-gui-tkinter/
class SchedulerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Study Scheduler")
        self.geometry("800x600")
        self.configure(bg="#ad87f8")
        self._init_styles()
        self.data_matrix = []
        self._build_main_ui()

    def _init_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', font=('Times New Roman', 14), padding=10)
        style.configure('Header.TLabel', font=('Times New Roman', 24, 'bold'), foreground='#333')

    def _build_main_ui(self):
        # Header Label
        header = ttk.Label(self, text="Smart Study Scheduler", style='Header.TLabel')
        header.pack(pady=20)

        # Button panel
        btn_panel = tk.Frame(self, bg="#ad87f8")
        btn_panel.pack(pady=10)

        self.load_data_btn = ttk.Button(btn_panel, text="Load Data", command=self.load_data, width=20)
        self.load_data_btn.pack(side=tk.LEFT, padx=10)

        self.analyze_btn = ttk.Button(btn_panel, text="Analyze Data", command=self.analyze_data, width=20)
        self.analyze_btn.pack(side=tk.LEFT, padx=10)

        # Task Table
        columns = ("Task #", "Days Til Due", "Duration", "Priority", "Energy Required", "Available Time", "Success")
        self.task_table = ttk.Treeview(self, columns=columns, show="headings", height=15)

        for col in columns:
            self.task_table.heading(col, text=col)
            self.task_table.column(col, anchor='center', width=100)

        self.task_table.pack(fill="both", expand=True, padx=20, pady=20)

    def load_data(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not filepath:
            return
        with open(filepath, "r") as f:
            data = json.load(f)

        self.data_matrix.clear()
        self.task_table.delete(*self.task_table.get_children())

        for task in data.get("tasks", []):
            row = [
                int(task["task_id"]),
                int(task["days_until_due"]),
                int(task["duration_in_minutes"]),
                int(task["priority_level"]),
                int(task["energy_required"]),
                int(task["available_time_minutes"]),
                int(task["success"])
            ]
            self.data_matrix.append(row)

            # Insert into Treeview
            self.task_table.insert("", tk.END, values=row)


    def analyze_data(self):
        if not self.data_matrix:
            messagebox.showerror("Error", "No data to analyze.")
            return

        data = np.array(self.data_matrix)

        priorities = data[:, 2]
        successes = data[:, 5]

        plt.figure()
        plt.scatter(priorities, successes)
        plt.xlabel("Priority (1-10)")
        plt.ylabel("Success (0=No, 1=Yes)")
        plt.title("Priority vs Success")
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    app = SchedulerGUI()
    app.mainloop()
