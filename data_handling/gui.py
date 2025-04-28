import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from dataclass_models import Task
from parse_data import load_json, parse_tasks, parse_energy_log, parse_availability
from functions_new import add_task, remove_task, generate_schedule, set_availability_log, set_energy_level, load_data

class SchedulerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Study Scheduler")
        self.geometry("900x650")
        self.configure(bg="#ad87f8")
        self._init_styles()
        self._build_splash()
        self._build_main_ui()
        self.show_splash()

    def _init_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', font=('Times New Roman', 14), padding=10)
        style.configure('Header.TLabel', font=('Times New Roman', 28, 'bold'), foreground='#333')
        style.configure('Treeview.Heading', font=('Times New Roman', 12, 'bold'))

    def _build_splash(self):
        self.splash_frame = tk.Frame(self, bg="#ad87f8")
        title = ttk.Label(self.splash_frame, text="Smart Study Scheduler", style='Header.TLabel')
        title.pack(pady=(100, 20))
        start_btn = ttk.Button(self.splash_frame, text="Start", command=self.show_main_ui)
        start_btn.pack(pady=10)

    def _build_main_ui(self):
        self.main_frame = tk.Frame(self, bg="#ad87f8")
        # Header
        header = ttk.Label(self.main_frame, text="Smart Study Scheduler", style='Header.TLabel')
        header.pack(pady=(20, 10))
        # Button panel
        btn_panel = tk.Frame(self.main_frame, bg="#ad87f8")
        btn_panel.pack(pady=15)
        self.load_data_btn = ttk.Button(btn_panel, text="Load Data", command=self.load_data, width=15)
        self.add_task_btn = ttk.Button(btn_panel, text="Add Task", command=self.add_task, width=15)
        self.remove_task_btn = ttk.Button(btn_panel, text="Remove Task", command=self.remove_task, width=15)
        self.generate_btn = ttk.Button(btn_panel, text="Generate Schedule", command=self.generate_schedule, width=18)
        for btn in [self.load_data_btn, self.add_task_btn, self.remove_task_btn, self.generate_btn]:
            btn.pack(side=tk.LEFT, padx=10)


    def show_splash(self):
        self.main_frame.pack_forget()
        self.splash_frame.pack(fill='both', expand=True)

    def show_main_ui(self):
        self.splash_frame.pack_forget()
        self.main_frame.pack(fill='both', expand=True)

    # reference for load_data: https://www.geeksforgeeks.org/python-askopenfile-function-in-tkinter/
    #                        : https://www.geeksforgeeks.org/python-gui-tkinter/
    def load_data(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if filepath:
            load_data(filepath)
            self.refresh_tasks_tree()

    def add_task(self):
        pass

    def remove_task(self):
        pass

    def generate_schedule(self):
        pass

if __name__ == "__main__":
    app = SchedulerGUI()
    app.mainloop()
