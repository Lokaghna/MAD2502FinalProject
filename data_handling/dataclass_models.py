import json
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any


# === Dataclass Models! ===

@dataclass
class Task:
    id: str

    days_until_due: int
    duration_in_minutes: int
    priority_level: int
    energy_required: int
    available_time_minutes: int
    success: int
    grade: float

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Task":
        return cls(
            id=data["task_id"],
            days_until_due=data["days_until_due"],
            duration_in_minutes=data["duration_in_minutes"],
            priority_level=data["priority_level"],
            energy_required=data["energy_required"],
            available_time_minutes=data["available_time_minutes"],
            grade=data["grade"],
            success=data["success"]
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.id,
            "days_until_due": self.days_until_due,
            "duration_in_minutes": self.duration_in_minutes,
            "priority_level": self.priority_level,
            "energy_required": self.energy_required,
            "available_time_minutes": self.available_time_minutes,
            "grade": self.grade,
            "success": self.success
        }

#@dataclass
#class EnergyEntry:
#    date: datetime
#    energy: int
#    notes: str
#    weekday: str
#
#@dataclass
#class AvailableBlock:
#    start: datetime
#    end: datetime

#@dataclass
#class DailyAvailability:
#    date: datetime
#    weekday: str
#    blocks: List[AvailableBlock]


def load_tasks(filepath: str) -> List[Task]:
    """
    Load JSON data from file
    """
    with open(filepath, "r") as f:
        rows = json.load(f)
    return [Task.from_json(r) for r in rows]