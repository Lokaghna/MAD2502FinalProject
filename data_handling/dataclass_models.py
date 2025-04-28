from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any


# === Dataclass Models! ===
# todo: could add @classmethods to convert between dataclass and dict for JSON
#  (JSON -> dict -> dataclass and vice versa) for import/export of data
#  also could have some individual functions for class specific things like:
#  a function for checking urgency of a Task

@dataclass
class Task:
    id: str
    title: str
    duration: float
    priority: int
    energy_required: int
    due_date: Optional[datetime]
    completed: bool

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Task":
        return cls(
            id=data["task_id"],
            title=data["title"],
            duration=data["estimated_duration_hours"],
            priority=data["priority"],
            energy_required=data["energy_required"],
            due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_data") else None,
            completed=data["completed"]
        )

    def to_dict(self) -> Dict[str, Any]:
        return{
            "task_id": self.id,
            "title": self.title,
            "estimated_duration_hours": self.duration,
            "priority": self.priority,
            "energy_required": self.energy_required,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed": self.completed
        }


@dataclass
class EnergyEntry:
    date: datetime
    energy: int

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "EnergyEntry":
        return cls(
            date=datetime.fromisoformat(data["date"]),
            energy=data["user_energy_level"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date.date().isoformat(),
            "user_energy_level":self.energy
        }


@dataclass
class AvailableBlock:
    start: datetime
    end: datetime

    @classmethod
    def from_json(cls, data: Dict[str, str], date_prefix: str) -> "AvailableBlock":
        # date_prefix will be the day since free blocks only give times
        start = datetime.fromisoformat(f"{date_prefix}T{data['start']}")
        end = datetime.fromisoformat(f"{date_prefix}T{data['end']}")
        return cls(start=start, end=end)

    def to_dict(self) -> Dict[str, str]:
        return {
            "start": self.start.strftime("%H:%M"),
            "end": self.end.strftime("%H:%M")
        }

@dataclass
class DailyAvailability:
    date: datetime
    blocks: List[AvailableBlock]

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "DailyAvailability":
        day_date = datetime.fromisoformat(data["date"])
        blocks = [AvailableBlock.from_json(block, data["date"]) for block in data["free_blocks"]]
        return cls(date=day_date, blocks=blocks)

    def to_dict(self) -> Dict[str, Any]:
        return{
            "date": self.date.date().isoformat(),
            "free_blocks": [block.to_dict() for block in self.blocks]
        }

# === Logic ===
# todo: figuring out models that could be good for showing predictive power of efficacy
#  SLR and MLR not really good enough since its hard to have a quantiative output of success in a task completion
#  so looked at logistic regression methods for possibly having a success metric (e.g rated at least a
#  7/10 on user rated self efficiency metric and was completed so-and-so time before the deadline, etc.)
#  One possibility is to have users give their choice of success metric and evaluate the probability of success for
#  tasks based on when they do them (main issue is that we don't have a lot of data)