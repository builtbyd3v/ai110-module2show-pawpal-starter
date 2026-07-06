from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    category: str = "general"
    recurring: bool = False


@dataclass
class Pet:
    name: str
    species: str
    age: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        pass


@dataclass
class PetOwner:
    name: str
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def update_preferences(self, preferences: List[str]) -> None:
        pass


@dataclass
class Scheduler:
    owner: PetOwner
    pet: Pet
    available_minutes: int = 60

    def build_daily_plan(self) -> List[Task]:
        pass

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        pass

    def explain_plan(self, tasks: List[Task]) -> List[str]:
        pass
