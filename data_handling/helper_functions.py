from dataclass_models import Task, load_tasks
from typing import Dict, List

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


