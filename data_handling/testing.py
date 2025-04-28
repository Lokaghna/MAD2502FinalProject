import numpy as np
n_rows = 10

duration_min = np.random.randint(10, 180, size=n_rows)
priority = np.random.randint(1, 11, size=n_rows)
energy_required = np.random.randint(1, 11, size=n_rows)
available_minutes = np.random.randint(30, 600, size=n_rows)
success = np.random.choice([0, 1], size=n_rows, p=[0.5, 0.5])

data_testing = []
for i in range(n_rows):
    data_testing.append({
        "task_name": f"Task {i + 1}",
        "duration_min": int(duration_min[i]),
        "priority": int(priority[i]),
        "energy_required": int(energy_required[i]),
        "available_minutes": int(available_minutes[i]),
        "success": int(success[i])
    })

columns = ["Task_Name", "Duration", "Priority", "Energy Requirements", "Available Minutes", "Success"]

key_mapping = {
    "Task_Name": "task_name",
    "Duration": "duration_min",
    "Priority": "priority",
    "Energy Requirements": "energy_required",
    "Available Minutes": "available_minutes",
    "Success": "success"
}
print("\t".join(columns))
for row in data_testing:
    print("\t".join(str(row[key_mapping[col]]) for col in columns))
