import numpy as np
n_rows = 10

duration_min = np.random.randint(10, 180, size=n_rows)
priority = np.random.randint(1, 11, size=n_rows)
energy_required = np.random.randint(1, 11, size=n_rows)
available_minutes = np.random.randint(30, 600, size=n_rows)
success = np.random.choice([0, 1], size=n_rows, p=[0.5, 0.5])

data_testing = []
for i in range(n_rows):
    row = [
        f"Task {i+1}",
        int(duration_min[i]),
        int(priority[i]),
        int(energy_required[i]),
        int(available_minutes[i]),
        int(success[i]),
    ]
    data_testing.append(row)

columns = ["Task_Name", "Duration", "Priority", "Energy Requirements", "Available Minutes", "Success"]
print("\t".join(columns))
for row in data_testing:
    print("\t".join(str(x) for x in row))
