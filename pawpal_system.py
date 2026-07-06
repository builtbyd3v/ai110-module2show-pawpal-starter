from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    """Store one care task and its scheduling details."""

    description: str
    duration_minutes: int
    priority: str
    time_of_day: Optional[str] = None
    category: str = "general"
    frequency: str = "daily"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""

        self.completed = True


@dataclass
class Pet:
    """Store one pet and its care tasks."""

    name: str
    species: str
    age: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""

        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return a copy of this pet's tasks."""

        return list(self.tasks)


@dataclass
class PetOwner:
    """Store the owner, their preferences, and their pets."""

    name: str
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""

        self.pets.append(pet)

    def update_preferences(self, preferences: List[str]) -> None:
        """Replace the owner's preferences."""

        self.preferences = list(preferences)

    def get_all_tasks(self) -> List[tuple[Pet, Task]]:
        """Return every task from every pet."""

        all_tasks: List[tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet, task))
        return all_tasks


@dataclass
class Scheduler:
    """Organize tasks from the owner into a daily plan."""

    owner: PetOwner
    available_minutes: int = 180
    start_time: str = "08:00"

    _priority_order = {"high": 0, "medium": 1, "low": 2}

    def _time_to_minutes(self, time_text: str) -> int:
        """Convert an HH:MM string into minutes from midnight."""

        hours, minutes = time_text.split(":")
        return int(hours) * 60 + int(minutes)

    def _minutes_to_time(self, total_minutes: int) -> str:
        """Convert minutes from midnight back into HH:MM format."""

        hours = (total_minutes // 60) % 24
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"

    def sort_tasks(self, tasks: List[tuple[Pet, Task]]) -> List[tuple[Pet, Task]]:
        """Sort tasks by priority, preferred time, and duration."""

        def sort_key(item: tuple[Pet, Task]) -> tuple[int, str, int, str, str]:
            pet, task = item
            priority_rank = self._priority_order.get(task.priority.lower(), 99)
            preferred_time = task.time_of_day or "23:59"
            return (
                priority_rank,
                preferred_time,
                task.duration_minutes,
                pet.name.lower(),
                task.description.lower(),
            )

        return sorted(tasks, key=sort_key)

    def build_daily_schedule(self) -> List[dict[str, str | int]]:
        """Build a schedule from all unfinished tasks that fit the time window."""

        scheduled_tasks: List[dict[str, str | int]] = []
        minutes_used = 0
        current_minutes = self._time_to_minutes(self.start_time)

        for pet, task in self.sort_tasks([
            item for item in self.owner.get_all_tasks() if not item[1].completed
        ]):
            if minutes_used + task.duration_minutes > self.available_minutes:
                continue

            start_minutes = current_minutes + minutes_used
            end_minutes = start_minutes + task.duration_minutes
            scheduled_tasks.append(
                {
                    "pet_name": pet.name,
                    "task_description": task.description,
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                    "start_time": self._minutes_to_time(start_minutes),
                    "end_time": self._minutes_to_time(end_minutes),
                    "frequency": task.frequency,
                }
            )
            minutes_used += task.duration_minutes

        return scheduled_tasks

    def explain_plan(self, tasks: List[dict[str, str | int]]) -> List[str]:
        """Explain why each scheduled task appears in the plan."""

        if not tasks:
            return ["No tasks fit within the available time window."]

        explanations: List[str] = []
        for item in tasks:
            explanations.append(
                f"{item['pet_name']}'s {item['task_description']} was included because it is {item['priority']} priority and fits in the available time."
            )
        return explanations
