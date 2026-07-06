from pathlib import Path

from tabulate import tabulate

from pawpal_system import Pet, PetOwner, Scheduler, Task, load_from_json, save_to_json

# ANSI color codes for terminal output
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_BLUE = "\033[94m"
COLOR_CYAN = "\033[96m"

# Emoji for task types
EMOJI_WALK = "🚶"
EMOJI_FOOD = "🍽️"
EMOJI_CLEAN = "🧹"
EMOJI_PLAY = "🎾"
EMOJI_HEALTH = "🏥"
EMOJI_HIGH = "🔴"
EMOJI_MEDIUM = "🟡"
EMOJI_LOW = "🟢"
EMOJI_CHECK = "✅"
EMOJI_CONFLICT = "⚠️"


def get_priority_emoji(priority: str) -> str:
    """Return emoji for priority level."""
    if priority.lower() == "high":
        return EMOJI_HIGH
    elif priority.lower() == "medium":
        return EMOJI_MEDIUM
    else:
        return EMOJI_LOW


def get_task_emoji(description: str) -> str:
    """Return emoji based on task description."""
    desc_lower = description.lower()
    if "walk" in desc_lower:
        return EMOJI_WALK
    elif "breakfast" in desc_lower or "feed" in desc_lower or "food" in desc_lower:
        return EMOJI_FOOD
    elif "clean" in desc_lower or "litter" in desc_lower:
        return EMOJI_CLEAN
    elif "play" in desc_lower or "enrichment" in desc_lower:
        return EMOJI_PLAY
    elif "vet" in desc_lower or "health" in desc_lower or "med" in desc_lower:
        return EMOJI_HEALTH
    return "📋"


def format_schedule_line(item: dict[str, str | int]) -> str:
    """Format one schedule item for terminal output."""
    priority_emoji = get_priority_emoji(str(item["priority"]))
    task_emoji = get_task_emoji(str(item["task_description"]))
    return (
        f"{item['start_time']} - {item['end_time']} | "
        f"{task_emoji} {item['pet_name']}: {item['task_description']} "
        f"{priority_emoji} ({item['duration_minutes']} min, {item['frequency']})"
    )


def format_task_label(pet: Pet, task: Task) -> str:
    """Format one task for the terminal demo."""
    priority_emoji = get_priority_emoji(task.priority)
    task_emoji = get_task_emoji(task.description)
    return [
        f"{task_emoji} {pet.name}",
        task.description,
        task.time_of_day or "—",
        f"{task.duration_minutes} min",
        f"{priority_emoji} {task.priority}",
    ]


def main() -> None:
    """Build and print a sample PawPal+ daily schedule."""

    owner = PetOwner(name="Jordan")
    dog = Pet(name="Mochi", species="dog", age=5)
    cat = Pet(name="Bean", species="cat", age=3)

    dog.add_task(Task("Morning walk", 30, "high", time_of_day="08:00"))
    dog.add_task(Task("Breakfast", 10, "high", time_of_day="08:30", frequency="daily"))
    cat.add_task(Task("Litter box check", 15, "medium", time_of_day="08:25"))
    cat.add_task(Task("Play session", 20, "low", time_of_day="10:00"))
    cat.add_task(Task("Vet reminder", 5, "low", time_of_day="08:30", frequency="weekly"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    data_path = Path("pawpal_data.json")
    save_to_json(owner, data_path)
    owner = load_from_json(data_path)

    scheduler = Scheduler(owner=owner, available_minutes=120, start_time="08:00")

    raw_tasks = owner.get_all_tasks()
    sorted_by_time = scheduler.sort_by_time(raw_tasks)
    filtered_for_mochi = scheduler.filter_tasks(raw_tasks, pet_name="Mochi")
    conflict_warnings = scheduler.detect_conflicts(raw_tasks)
    schedule = scheduler.build_daily_schedule()
    explanations = scheduler.explain_plan(schedule)

    print(f"\n{COLOR_BOLD}{COLOR_BLUE}Unsorted task list{COLOR_RESET}")
    print(COLOR_BLUE + "—" * 40 + COLOR_RESET)
    raw_table = [format_task_label(pet, task) for pet, task in raw_tasks]
    print(tabulate(raw_table, headers=["Pet", "Description", "Time", "Duration", "Priority"], tablefmt="grid"))

    print(f"\n{COLOR_BOLD}{COLOR_CYAN}Sorted by time{COLOR_RESET}")
    print(COLOR_CYAN + "—" * 40 + COLOR_RESET)
    sorted_table = [format_task_label(pet, task) for pet, task in sorted_by_time]
    print(tabulate(sorted_table, headers=["Pet", "Description", "Time", "Duration", "Priority"], tablefmt="grid"))

    print(f"\n{COLOR_BOLD}{COLOR_CYAN}Filtered for Mochi{COLOR_RESET}")
    print(COLOR_CYAN + "—" * 40 + COLOR_RESET)
    filtered_table = [format_task_label(pet, task) for pet, task in filtered_for_mochi]
    print(tabulate(filtered_table, headers=["Pet", "Description", "Time", "Duration", "Priority"], tablefmt="grid"))

    print(f"\n{COLOR_BOLD}{COLOR_YELLOW}Conflict warnings{COLOR_RESET}")
    print(COLOR_YELLOW + "—" * 40 + COLOR_RESET)
    if conflict_warnings:
        for warning in conflict_warnings:
            print(f"{EMOJI_CONFLICT} {COLOR_RED}{warning}{COLOR_RESET}")
    else:
        print(f"{COLOR_GREEN}{EMOJI_CHECK} No conflicts found.{COLOR_RESET}")

    print(f"\n{COLOR_BOLD}{COLOR_GREEN}Today's Schedule{COLOR_RESET}")
    print(COLOR_GREEN + "—" * 40 + COLOR_RESET)
    for item in schedule:
        print(format_schedule_line(item))

    print(f"\n{COLOR_BOLD}{COLOR_YELLOW}Why this plan was chosen{COLOR_RESET}")
    print(COLOR_YELLOW + "—" * 40 + COLOR_RESET)
    for i, explanation in enumerate(explanations, 1):
        print(f"{i}. {explanation}")

    print(f"\n{COLOR_BOLD}{COLOR_CYAN}Recurring tasks after scheduling{COLOR_RESET}")
    print(COLOR_CYAN + "—" * 40 + COLOR_RESET)
    recurring_table = []
    for pet in owner.pets:
        for task in pet.tasks:
            recurring_table.append(format_task_label(pet, task))
    print(tabulate(recurring_table, headers=["Pet", "Description", "Time", "Duration", "Priority"], tablefmt="grid"))

    print(f"\n{COLOR_GREEN}{EMOJI_CHECK} Saved and reloaded data from: {data_path}{COLOR_RESET}")


if __name__ == "__main__":
    main()