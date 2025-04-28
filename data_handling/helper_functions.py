from dataclass_models import Task, load_tasks
from typing import Dict, List
import numpy as np

tasks: List[Task] = []

def load_data(filepath: str) -> None:
    """
    Load tasks, energy log, and availability log from a JSON file into program memory.
    """
    data = load_tasks(filepath)
    task_list: list[Task] = data
    # energy_entries = parse_energy_log(data)
    # availability = parse_availability(data)

    global tasks
    tasks.clear()
    tasks.extend(task_list)

def analyze_feature_vs_grade(tasks: List[Task], feature_name: str) -> tuple[np.ndarray, np.ndarray]:
    """
    Analyze a selected feature vs success.
    """
    # map features to task attribute names
    feature_mapping = {
        "Priority Level": "priority_level",
        "Energy Required": "energy_required",
        "Available Time": "available_time_minutes",
        "Days Until Due": "days_until_due",
        "Duration": "duration_in_minutes"
    }
    # check is feature is valid
    if feature_name not in feature_mapping:
        raise ValueError(f"Unknown feature: {feature_name}")

    x_attr = feature_mapping[feature_name]

    x_values = np.array([getattr(task, x_attr) for task in tasks])
    y_values = np.array([task.grade for task in tasks])

    return x_values, y_values