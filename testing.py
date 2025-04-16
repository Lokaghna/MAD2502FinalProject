from asyncio import Task, tasks


def add_task(task_info: Task) -> None:
    tasks.append(task_info)

def remove_task(task_info: int) -> None:
    tasks.pop(task_info)

def set_energy_level(energy_data: Dict[str, float]) -> None:
    global energy_profile
    energy_profile = energy_data

def set_user_availability(availability_info: Dict[str, List[TimeSlot]]) -> None:
    global user_availability
    user_availability = availability_info

def generate_schedule() -> Dict[]:
