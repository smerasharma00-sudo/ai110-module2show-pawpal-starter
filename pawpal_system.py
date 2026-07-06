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

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return warning messages for tasks that overlap or duplicate."""
        warnings = []
        seen_titles = set()

        for task in tasks:
            if task.title in seen_titles:
                warnings.append(f"Duplicate task detected: '{task.title}' appears more than once.")
            seen_titles.add(task.title)

        return warnings

    def explain_plan(self, plan: List[Task]) -> List[str]:
        """Return a human-readable reason for each task's inclusion in the plan."""
        explanations = []
        for task in plan:
            explanations.append(
                f"Included '{task.title}' ({task.duration_minutes} min, {task.priority} priority)."
            )
        return explanations

