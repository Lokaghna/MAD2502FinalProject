from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


# === Dataclass Models! ===
# todo: could add @classmethods to convert between dataclass and dict for JSON
#  (JSON -> dict -> dataclass and vice versa) for import/export of data
#  also could have some individual functions for class specific things like:
#  a function for checking urgency of a Task

@dataclass
class Task:
    id: str
    title: str
    category: str
    duration: float
    priority: str
    # todo: ^ a bit unsure of what this could be, maybe a low, medium, high for qualitative data?
    #  or another numerical rating for quantitative
    energy_required: int
    due_date: Optional[datetime]
    scheduled: Optional[datetime]
    completed: bool
    weekday_due: Optional[str]
    weekday_scheduled: Optional[str]

@dataclass
class EnergyEntry:
    date: datetime
    energy: int
    notes: str
    weekday: str

@dataclass
class AvailableBlock:
    start: datetime
    end: datetime

@dataclass
class DailyAvailability:
    date: datetime
    weekday: str
    blocks: List[AvailableBlock]


# === Logic ===
# todo: figuring out models that could be good for showing predictive power of efficacy
#  SLR and MLR not really good enough since its hard to have a quantiative output of success in a task completion
#  so looked at logistic regression methods for possibly having a success metric (e.g rated at least a
#  7/10 on user rated self efficiency metric and was completed so-and-so time before the deadline, etc.)
#  One possibility is to have users give their choice of success metric and evaluate the probability of success for
#  tasks based on when they do them (main issue is that we don't have a lot of data)