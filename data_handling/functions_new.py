from dataclass_models import Task, EnergyEntry, AvailableBlock, DailyAvailability
from typing import Dict, List
from datetime import timedelta, datetime
from parse_data import load_json, parse_tasks, parse_energy_log, parse_availability


tasks: List[Task] = []


def load_data(filepath: str) -> None:
    """
    Load tasks, energy log, and availability log from a JSON file into program memory.
    """
    data = load_json(filepath)
    task_list = parse_tasks(data)
    # energy_entries = parse_energy_log(data)
    # availability = parse_availability(data)

    global tasks, energy_log, availability_log, energy_profile
    tasks.clear()
    tasks.extend(task_list)

    energy_log.clear()
    energy_log.extend(energy_entries)

    availability_log.clear()
    availability_log.extend(availability)

    energy_profile.clear()
    for entry in energy_entries:
        hour_str = entry.date.strftime("%H:00")
        energy_profile[hour_str] = entry.energy




# energy_log: List[EnergyEntry] = []
# availability_log: List[DailyAvailability] = []
# energy_profile: Dict[str,float] = {}
#
# def add_task(task_info: Task) -> None:
#     """Add a task to the user's task list:
#     Parameters: task_info (Task): A Task object containing details such as task id or task name"""
#     tasks.append(task_info)
#
# def remove_task(task_id: int) -> None:
#     """Remove a task from the user's task list (probably by index?)
#     Parameters: task_info (int): A Task object containing details such as task id or task name"""
#     for i, task in enumerate(tasks):
#         if task.id == task_id:
#             tasks.pop(i)
#
# def set_availability_log(log:List [DailyAvailability]) -> None:
#     global availability_log
#     availability_log = log
#
# def priority_to_number(priority: str) -> int:
#     mapping = {"low" : 1, "medium" : 2, "high" : 3}
#     return mapping.get(priority.lower(), 0)
#
# def set_energy_level(energy_data: Dict[str, float]) -> None:
#     """Sets the user's energy profile throughout a day
#     Parameters: energy_data (Dict[str, float]): A dictionary containing energy profile details,
#     where higher energy indicate higher energy levels"""
#     global energy_profile
#     energy_profile = energy_data
#
# def get_average_energy(block: AvailableBlock) -> float:
#     start = block.start
#     end = block.end
#     total_energy = 0.0
#     total_duration = 0.0
#     current = start
#     while current < end:
#         next_hour = (current + timedelta(hours=1)).replace(minute = 0, second = 0) #In case energy is different in different hours
#         if next_hour > end:
#             next_hour = end
#         time_in_hour = (next_hour - current).total_seconds()/3600
#         hour_str = current.strftime("%H:00")
#         if hour_str in energy_profile:
#             total_energy += energy_profile[hour_str] * time_in_hour
#             total_duration += time_in_hour
#         current = next_hour
#     return total_energy / total_duration if total_duration > 0 else 0.0
#
# def generate_schedule() -> Dict[str, List[AvailableBlock]]: #refer to Loki's AvailableBlock class
#     schedule: Dict[str, List[AvailableBlock]] = {}
#     sorted_task = sorted(tasks, key=lambda t: (t.due_date if t.due_date else datetime.max, -priority_to_number(t.priority)))
#     for task in sorted_task:
#         remaining = task.duration
#         schedule[task.title] = []
#
#         for day in availability_log:
#             if task.due_date is not None and day.date.date() > task.due_date.date():
#                 break
#             i = 0
#             while i < len(day.blocks) and remaining > 0:
#                 block = day.blocks[i]
#                 if task.due_date is not None and block.end > task.due_date:
#                     i += 1
#                     continue
#                 average_energy = get_average_energy(block)
#                 if average_energy > task.energy_required:
#                     block_duration = (block.end - block.start).total_seconds()/3600
#                     if remaining <= block_duration:
#                         assign_end = block.start + timedelta(hours = remaining)
#                         assigned_block = AvailableBlock(start = block.start, end = assign_end)
#
#                         schedule[task.title].append(assigned_block)
#                         block.start = assign_end
#                         if block.start >= block.end:
#                             del day.blocks[i]
#
#                         else:
#                             i += 1
#                         remaining = 0
#                     else:
#                         schedule[task.title].append(block)
#                         remaining -= block_duration
#                         del day.blocks[i]
#                 else:
#                     i += 1
#     return schedule