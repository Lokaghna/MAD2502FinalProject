from dataclass_models import Task, load_tasks
import numpy as np
import json

n_rows = 100
days_until_due = np.random.randint(1, 15, size=n_rows)
duration_min = np.random.randint(10, 120, size=n_rows)
priority = np.random.randint(1, 11, size=n_rows)
energy_required = np.random.randint(1, 11, size=n_rows)
available_minutes = np.random.randint(100, 360, size=n_rows)
success = np.random.choice([0,0], size=n_rows)
grade = np.random.randint(1,  100, size=n_rows)

data_testing = []
for i in range(n_rows):
    data_testing.append({
         "task_id": i + 1,
        "days_until_due": int(days_until_due[i]),
        "duration_in_minutes": int(duration_min[i]),
        "priority_level": int(priority[i]),
        "energy_required": int(energy_required[i]),
        "available_time_minutes": int(available_minutes[i]),
        "grade": int(grade[i]),
        "success": 1 if(grade[i] >= 70) else 0
    })


# Save to JSON file
with open("test_tasks.json", "w") as f:
    json.dump(data_testing, f, indent=4)
