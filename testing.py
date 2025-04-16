from asyncio import Task, tasks


def add_task(task_info: Task) -> None:
    """Add a task to the user's task list:
    Parameters: task_info (Task): A Task object containing details such as task id or task name"""
    tasks.append(task_info)

def remove_task(task_info: int) -> None:
    """Remove a task from the user's task list (probably by index?)
    Parameters: task_info (int): A Task object containing details such as task id or task name"""
    tasks.pop(task_info)

def set_energy_level(energy_data: Dict[str, float]) -> None:
    """Sets the user's energy profile throughout a day
    Parameters: energy_data (Dict[str, float]): A dictionary containing energy profile details,
    where higher energy indicate higher energy levels"""
    global energy_profile
    energy_profile = energy_data

def set_user_availability(availability_info: Dict[str, List[TimeSlot]]) -> None:
    """Define the user's availability for scheduling tasks
    Parameters: availability_info (Dict[str, List[TimeSlot]]): A dictionary mapping days of the week to
    a list of TimeSlot objects showing when the user is free"""
    global user_availability
    user_availability = availability_info

def generate_schedule() -> Dict[]:
