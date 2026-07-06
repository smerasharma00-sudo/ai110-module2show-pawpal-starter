from dataclasses import dataclass, field
from typing import List, Optional

PRIORITY_WEIGHT = {"high": 3, "medium": 2, "low": 1}

@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "once"
    is_complete: bool = False
    start_time: Optional[str] = None  # "HH:MM" format, e.g. "08:00"

    def mark_complete(self):
        """Mark this task as complete."""
        self.is_complete = True
@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks
@dataclass
class Owner:
    name: str
    available_minutes_per_day: int = 120
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks
class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted from highest to lowest priority."""
        return sorted(tasks, key=lambda task: PRIORITY_WEIGHT[task.priority], reverse=True)

    def build_daily_plan(self) -> List[Task]:
        """Greedily select tasks by priority until available_minutes_per_day is used up."""
        all_tasks = self.owner.get_all_tasks()
        sorted_tasks = self.sort_by_priority(all_tasks)

        plan = []
        minutes_used = 0
        budget = self.owner.available_minutes_per_day

        for task in sorted_tasks:
            if task.is_complete:
                continue
            if minutes_used + task.duration_minutes <= budget:
                plan.append(task)
                minutes_used += task.duration_minutes

        return plan
    def get_next_occurrence(self, task: Task) -> Optional[Task]:
        """If a completed daily/weekly task recurs, return the next instance."""
        if not task.is_complete or task.frequency == "once":
            return None
        return Task(
            title=task.title,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            frequency=task.frequency,
            is_complete=False,
            start_time=task.start_time,
        )
    

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return warning messages for tasks whose time windows overlap."""
        warnings = []
        timed_tasks = [t for t in tasks if t.start_time is not None]

        def to_minutes(hhmm: str) -> int:
            h, m = hhmm.split(":")
            return int(h) * 60 + int(m)

        intervals = []
        for t in timed_tasks:
            start = to_minutes(t.start_time)
            end = start + t.duration_minutes
            intervals.append((start, end, t))

        intervals.sort(key=lambda x: x[0])

        for i in range(len(intervals) - 1):
            start_a, end_a, task_a = intervals[i]
            start_b, end_b, task_b = intervals[i + 1]
            if start_b < end_a:
                warnings.append(
                    f"Conflict: '{task_a.title}' and '{task_b.title}' overlap in time."
                )

        return warnings
