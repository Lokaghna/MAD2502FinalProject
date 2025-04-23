from dataclass_models import Task, EnergyEntry, AvailableBlock, DailyAvailability
from typing import Dict, List
from datetime import timedelta


tasks: List[Task] = []
energy_log: List[EnergyEntry] = []
availability_log: List[DailyAvailability] = []
energy_profile: Dict[str,float] = {}
def add_task(task_info: Task) -> None:
    """Add a task to the user's task list:
    Parameters: task_info (Task): A Task object containing details such as task id or task name"""
    tasks.append(task_info)

def remove_task(task_index: int) -> None:
    """Remove a task from the user's task list (probably by index?)
    Parameters: task_info (int): A Task object containing details such as task id or task name"""
    if 0 <= task_index <= len(tasks):
        tasks.pop(task_index)
def set_energy_log(log:List [EnergyEntry]) -> None:
    global energy_log
    energy_log = log
def set_availability_log(log:List [DailyAvailability]) -> None:
    global availability_log
    availability_log = log
def priority_to_number(priority: int) -> int:
    mapping = {"low" : 1, "medium" : 2, "high" : 3}
    return mapping.get(priority, 0)
def set_energy_level(energy_data: Dict[str, float]) -> None:
    """Sets the user's energy profile throughout a day
    Parameters: energy_data (Dict[str, float]): A dictionary containing energy profile details,
    where higher energy indicate higher energy levels"""
    global energy_profile
    energy_profile = energy_data

def generate_schedule() -> Dict[str, List[AvailableBlock]]: #refer to Loki's AvailableBlock class
    schedule: Dict[str, List[AvailableBlock]] = {}
    sorted_task = sorted(tasks, key=lambda t: -priority_to_number(t.priority))
    for task in sorted_task:
        remaining = task.duration
        for day in availability_log:
            if remaining <= 0:
                break
            for block in day.blocks:
                block_duration = (block.end - block.start).total_seconds() / 3600
                if remaining <= 0:
                    break
                if block_duration >= remaining:
                    assigned_block = AvailableBlock(start = block.start, end = block.start + timedelta(hours = remaining))
                    schedule[task.title].append(assigned_block)
                    remaining = 0
                else:
                    schedule[task.title].append(block)
                    remaining -= block_duration
    return schedule


