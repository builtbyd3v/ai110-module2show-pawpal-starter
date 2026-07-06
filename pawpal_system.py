from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
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

    def next_occurrence(self) -> Optional[Task]:
        """Return the next repeating instance for daily or weekly tasks."""

        if self.frequency == "daily":
            return Task(
                description=self.description,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                time_of_day=self.time_of_day,
                category=self.category,
                frequency=self.frequency,
            )
        if self.frequency == "weekly":
            return Task(
                description=self.description,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                time_of_day=self.time_of_day,
                category=self.category,
                frequency=self.frequency,
            )
        return None

    def to_dict(self) -> dict[str, str | int | bool | None]:
        """Convert the task into JSON-friendly data."""

        return {
            "description": self.description,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "time_of_day": self.time_of_day,
            "category": self.category,
            "frequency": self.frequency,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str | int | bool | None]) -> Task:
        """Build a task from JSON-friendly data."""

        return cls(
            description=str(data.get("description", "Untitled task")),
            duration_minutes=int(data.get("duration_minutes", 0)),
            priority=str(data.get("priority", "low")),
            time_of_day=data.get("time_of_day") if data.get("time_of_day") is not None else None,
            category=str(data.get("category", "general")),
            frequency=str(data.get("frequency", "daily")),
            completed=bool(data.get("completed", False)),
        )


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

    def remove_completed_tasks(self) -> None:
        """Remove completed tasks after they have been handled."""

        self.tasks = [task for task in self.tasks if not task.completed]

    def get_tasks(self) -> List[Task]:
        """Return a copy of this pet's tasks."""

        return list(self.tasks)

    def to_dict(self) -> dict[str, str | int | list[dict[str, str | int | bool | None]] | None]:
        """Convert the pet into JSON-friendly data."""

        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Pet:
        """Build a pet from JSON-friendly data."""

        pet = cls(
            name=str(data.get("name", "Unnamed pet")),
            species=str(data.get("species", "other")),
            age=data.get("age") if isinstance(data.get("age"), int) else None,
        )
        for task_data in data.get("tasks", []):
            if isinstance(task_data, dict):
                pet.add_task(Task.from_dict(task_data))
        return pet


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

    def get_tasks_for_pet(self, pet_name: str) -> List[Task]:
        """Return tasks for a single pet by name."""

        for pet in self.pets:
            if pet.name == pet_name:
                return pet.get_tasks()
        return []

    def to_dict(self) -> dict[str, object]:
        """Convert the owner tree into JSON-friendly data."""

        return {
            "name": self.name,
            "preferences": list(self.preferences),
            "pets": [pet.to_dict() for pet in self.pets],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> PetOwner:
        """Build an owner tree from JSON-friendly data."""

        owner = cls(name=str(data.get("name", "Jordan")))
        preferences = data.get("preferences", [])
        if isinstance(preferences, list):
            owner.preferences = [str(item) for item in preferences]
        pets = data.get("pets", [])
        if isinstance(pets, list):
            for pet_data in pets:
                if isinstance(pet_data, dict):
                    owner.add_pet(Pet.from_dict(pet_data))
        return owner


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

    def find_next_available_slot(
        self,
        scheduled_tasks: List[dict[str, str | int]],
        duration_minutes: int,
        preferred_time: Optional[str] = None,
    ) -> Optional[str]:
        """Find the next open start time for a task."""

        start_minutes = self._time_to_minutes(preferred_time or self.start_time)
        current_minutes = start_minutes

        ordered_schedule = sorted(scheduled_tasks, key=lambda item: str(item["start_time"]))
        for item in ordered_schedule:
            item_start = self._time_to_minutes(str(item["start_time"]))
            item_end = self._time_to_minutes(str(item["end_time"]))

            if current_minutes + duration_minutes <= item_start:
                return self._minutes_to_time(current_minutes)
            if current_minutes < item_end:
                current_minutes = item_end

        if current_minutes + duration_minutes <= self._time_to_minutes("23:59"):
            return self._minutes_to_time(current_minutes)
        return None

    def sort_by_time(self, tasks: List[tuple[Pet, Task]]) -> List[tuple[Pet, Task]]:
        """Sort tasks by their preferred time, then by priority."""

        def sort_key(item: tuple[Pet, Task]) -> tuple[str, int, str, str]:
            pet, task = item
            preferred_time = task.time_of_day or "23:59"
            priority_rank = self._priority_order.get(task.priority.lower(), 99)
            return (preferred_time, priority_rank, pet.name.lower(), task.description.lower())

        return sorted(tasks, key=sort_key)

    def filter_tasks(
        self,
        tasks: List[tuple[Pet, Task]],
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> List[tuple[Pet, Task]]:
        """Filter tasks by pet name or completion status."""

        filtered_tasks = tasks
        if pet_name is not None:
            filtered_tasks = [item for item in filtered_tasks if item[0].name == pet_name]
        if completed is not None:
            filtered_tasks = [item for item in filtered_tasks if item[1].completed == completed]
        return filtered_tasks

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

    def detect_conflicts(self, tasks: List[tuple[Pet, Task]]) -> List[str]:
        """Warn when two tasks overlap at the same preferred time."""

        warnings: List[str] = []
        sorted_tasks = self.sort_by_time(tasks)

        for index, (left_pet, left_task) in enumerate(sorted_tasks):
            if left_task.time_of_day is None:
                continue
            left_start = self._time_to_minutes(left_task.time_of_day)
            left_end = left_start + left_task.duration_minutes

            for right_pet, right_task in sorted_tasks[index + 1 :]:
                if right_task.time_of_day is None:
                    continue
                right_start = self._time_to_minutes(right_task.time_of_day)
                right_end = right_start + right_task.duration_minutes

                if right_start < left_end and left_start < right_end:
                    warnings.append(
                        f"Conflict: {left_pet.name}'s {left_task.description} overlaps with {right_pet.name}'s {right_task.description}."
                    )

        return warnings

    def build_daily_schedule(self) -> List[dict[str, str | int]]:
        """Build a schedule from all unfinished tasks that fit the time window."""

        scheduled_tasks: List[dict[str, str | int]] = []
        minutes_used = 0
        current_minutes = self._time_to_minutes(self.start_time)

        eligible_tasks = self.filter_tasks(self.owner.get_all_tasks(), completed=False)

        for pet, task in self.sort_tasks(eligible_tasks):
            if minutes_used + task.duration_minutes > self.available_minutes:
                continue

            start_minutes = current_minutes + minutes_used
            next_slot = self.find_next_available_slot(scheduled_tasks, task.duration_minutes, task.time_of_day)
            if next_slot is not None:
                start_minutes = self._time_to_minutes(next_slot)
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

            task.mark_complete()
            recurring_task = task.next_occurrence()
            if recurring_task is not None:
                pet.add_task(recurring_task)
            pet.remove_completed_tasks()

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


def save_to_json(owner: PetOwner, file_path: str | Path) -> None:
    """Save the current owner tree to disk as JSON."""

    path = Path(file_path)
    path.write_text(json.dumps(owner.to_dict(), indent=2), encoding="utf-8")


def load_from_json(file_path: str | Path) -> PetOwner:
    """Load an owner tree from a JSON file."""

    path = Path(file_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Invalid PawPal+ JSON data")
    return PetOwner.from_dict(data)
