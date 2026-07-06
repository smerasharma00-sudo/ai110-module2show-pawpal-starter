from dataclasses import dataclass, field
from typing import List, Optional
@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "once"
    is_complete: bool = False

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
        pass

    def build_daily_plan(self) -> List[Task]:
        """Greedily select tasks by priority until available_minutes_per_day is used up."""
        pass

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return warning messages for tasks that overlap or duplicate."""
        pass

    def explain_plan(self, plan: List[Task]) -> List[str]:
        """Return a human-readable reason for each task's inclusion in the plan."""
        pass
