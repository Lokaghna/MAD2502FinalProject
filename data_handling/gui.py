import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
from helper_functions import load_data, tasks, analyze_feature_vs_grade
from math_logic import fit_beta_success,fit_beta_grade, predict_prob


# reference for gui: https://www.geeksforgeeks.org/python-gui-tkinter/
class SchedulerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Daily Planner")
        self.geometry("800x600") # window size
        self.configure(bg="#ad87f8") # sets background color
        self._init_styles()
        self.data_matrix = [] # storage of task data
        self._build_main_ui()

    # reference for button styling: https://www.geeksforgeeks.org/python-add-style-to-tkinter-button/
    def _init_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', font=('Times New Roman', 14), padding=10)
        style.configure('Header.TLabel', font=('Times New Roman', 24, 'bold'), foreground='#333')

    def _build_main_ui(self):
        # header Label
        header = ttk.Label(self, text="Smart Daily Planner", style='Header.TLabel')
        header.pack(pady=20)

        # button panel
        btn_panel = tk.Frame(self, bg="#ad87f8")
        btn_panel.pack(pady=10)

        # load data button
        self.load_data_btn = ttk.Button(btn_panel, text="Load Data", command=self.load_data, width=20)
        self.load_data_btn.pack(side=tk.LEFT, padx=10)

        # analyze data button
        self.analyze_btn = ttk.Button(btn_panel, text="Analyze Data", command=self.analyze_data, width=20)
        self.analyze_btn.pack(side=tk.LEFT, padx=10)

        # probability button
        self.probability_btn = ttk.Button(btn_panel, text="Calculate Success", command=self.calculate_prob, width=20)
        self.probability_btn.pack(side=tk.LEFT, padx=10)

        # task table
        columns = ("Task #", "Days Til Due", "Duration", "Priority", "Energy Required", "Available Time", "Grade")
        self.task_table = ttk.Treeview(self, columns=columns, show="headings", height=15)

        for col in columns:
            self.task_table.heading(col, text=col)
            self.task_table.column(col, anchor='center', width=100)

        self.task_table.pack(fill="both", expand=True, padx=20, pady=20)

    #reference for askopenfilename: https://www.geeksforgeeks.org/python-askopenfile-function-in-tkinter/
    def load_data(self):
        """
        handles loading tasks from JSON file and displaying them in table
        """
        filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not filepath:
            return
        # tasks loaded into global tasks list
        load_data(filepath)

        self.data_matrix.clear()
        self.task_table.delete(*self.task_table.get_children())

        # insert uploaded data to table
        for task in tasks:
            row = [
                int(task.id),
                int(task.days_until_due),
                int(task.duration_in_minutes),
                int(task.priority_level),
                int(task.energy_required),
                int(task.available_time_minutes),
                int(task.grade)
            ]
            self.data_matrix.append(row)

            self.task_table.insert("", tk.END, values=row)

    def analyze_data(self):
        """
        analyze selected feature vs grade and creates scatter plots
        """
        if not self.data_matrix:
            messagebox.showerror("Error", "No data to analyze.")
            return

        feature_list = ["Priority Level", "Energy Required", "Available Time", "Days Until Due", "Duration"]

        # scatter plots for each feature
        for feature_name in feature_list:
            x_values, y_values = analyze_feature_vs_grade(tasks, feature_name)

            plt.figure(figsize=(8, 5))
            plt.scatter(x_values, y_values, s=50, alpha=0.7, edgecolors='k')
            plt.xlabel(feature_name, fontsize=12)
            plt.ylabel("Grade (In Percent)", fontsize=12)
            plt.title(f"{feature_name} vs Grade", fontsize=14)
            plt.ylim(0, 100)
            plt.yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
            plt.grid(True)

        # display all plots after generated
        plt.show()

        # https://docs.python.org/3/library/dialog.html
        # tkinter user input stuff using simpledialog
    def calculate_prob(self):
        """
        calculates probability of success for a new task and predicted grade
        """
        self.beta_success = fit_beta_success(tasks)
        self.beta_grade = fit_beta_grade(tasks)
        try:
            vals = {
                "days_until_due": int(simpledialog.askinteger("Input", "How many days until due?")),
                "duration_in_minutes": int(simpledialog.askinteger("Input", "How long do you expect it to take (in minutes)?")),
                "priority_level": int(simpledialog.askinteger("Input", "What is the task's priority level (from 1-10)?")),
                "energy_required": int(simpledialog.askinteger("Input", "What is the expected energy requirement (from 1-10)?")),
                "available_time_minutes": int(simpledialog.askinteger("Input", "How much time do you have available today (in minutes)?"))
            }
        except ValueError:
            ValueError("Bad input, invalid integer")
            return

        prob, z, grade = predict_prob(self.beta_success,self.beta_grade, vals)

        messagebox.showinfo("Outcome: ", f"You have a success probability of {prob*100:.3f}%! and expected grade of {grade:.3f}.")

if __name__ == "__main__":
    app = SchedulerGUI()
    app.mainloop()
