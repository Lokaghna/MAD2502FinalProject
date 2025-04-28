import json
import calendar
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclass_models import Task, EnergyEntry, AvailableBlock, DailyAvailability

# === Load JSON ===

# todo: check logic of load, do we want to save to a specific place or just read it
#  parse it, and then just close it

def load_json(filepath: str) -> Dict[str, Any]:
    """
    Load JSON data from file
    """
    with open(filepath, "r") as f:
        return json.load(f)


# === Calendar Stuff ===
# https://docs.python.org/3/library/datetime.html
# https://docs.python.org/3/library/calendar.html

def parse_datetime(date_str: str) -> datetime:
    """
    Convert date string to datetime object
    :param date_str: str of date
    :return: datetime object
    :exception: ValueError if date format isn't right
    """
    formats = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date format not recognized: {date_str}")


def get_weekday_name(date_obj: datetime) -> str:
    """
    Get weekday name
    :param date_obj: datetime object
    :return: str of day ("Monday")
    """
    return calendar.day_name[date_obj.weekday()]


# === Parse data for Models ===
# todo: add conversion of or calling of information as dataclass methods
#   also should figure out what other functionalities are most needed as we move forward.

def parse_energy_log(data: Dict[str, Any]) -> List[EnergyEntry]:
    """
    Parse energy_log section of JSON
    :param data: input of data log
    :return: returns list of energy entry objects
    """
    energy_log = []
    for entry in data.get("energy_log", []):
        energy_log.append(EnergyEntry(
            date=parse_datetime(entry["date"]),
            energy=entry["energy_level"],
            notes=entry.get("notes", ""),
            weekday=get_weekday_name(parse_datetime(entry["date"]))
        ))
    return energy_log


def parse_tasks(data: Dict[str, Any]) -> List[Task]:
    """
    Parse tasks section of the JSON
    :param data: input of data log
    :return: list of task objects
    """
    tasks = []
    for task in data.get("tasks", []):
        due = parse_datetime(task["due_date"] if task["due_date"] else None)
        scheduled = parse_datetime(task["date_scheduled"] if task["date_scheduled"] else None)
        tasks.append(Task(
            id=task["task_id"],
            title=task["title"],
            category=task["category"],
            duration=task["estimated_duration_hours"],
            priority=task["priority"],
            energy_required=task["energy_required"],
            due_date=due,
            scheduled=scheduled,
            completed=task["completed"],
            weekday_due = get_weekday_name(due) if due else None,
            weekday_scheduled=get_weekday_name(scheduled) if scheduled else None
        ))
    return tasks


def parse_availability(data: Dict[str, Any]) -> List[DailyAvailability]:
    """
    Parse daily abilability section of JSON
    :param data: input of data log
    :return: list of daily abailability objects
    """
    avail = []
    for day in data.get("availability", []):
        day_obj = parse_datetime(day["date"])
        blocks = []
        for block in day["free_blocks"]:
            blocks.append(AvailableBlock(
                start=datetime.strptime(f"{day['date']} {block['start']}", "%Y-%m-$d %H:%M"),
                end=datetime.strptime(f"{day['date']} {block['end']}", "%Y-%m-%d %H:%M")
            ))
        avail.append(DailyAvailability(
            date=day_obj,
            weekday=get_weekday_name(day_obj),
            blocks=blocks
        ))

    return avail